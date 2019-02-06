import asyncio
import requests

import random, string

import json
from aiogram.types.message import ContentType

from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from aiogram.utils import markdown
import config

from db_module import db_main, db_config
from keyboard_module import keyboard_main


import threading

import math

bot = Bot(token=config.telegram_token)
dp = Dispatcher(bot)

tables = db_config.tables()

categories = []
count_items = []
admins = []
texts = {}
# need update sometimes!!!!
forward_target = 0 # 0 - add manager, 1 - add chat

def generate_kb(category_id, position, photo_message_id, scroll = True):
    global categories
    global count_items

    count = count_items[category_id-1]
    print ("_____")
    print (count, type(count))
    print ("_____")

    position_left = position - 1
    if position_left < 1:
        position_left = count

    position_right = position + 1
    if position_right > count:
        position_right = 1

    keyboard = []; callback = []

    if scroll == True:
        keyboard.append(["<<", "{position}/{count}".format(position=position, count=count), ">>"])
        callback.append([
                "catalog_item {category_id} {position} {photo_message_id}".format(category_id=category_id, position=position_left, photo_message_id=photo_message_id),
                "scroll {category_id} {position} {photo_message_id} 0".format(category_id=category_id, position=position, photo_message_id=photo_message_id),
                "catalog_item {category_id} {position} {photo_message_id}".format(category_id=category_id, position=position_right, photo_message_id=photo_message_id)
            ])
    else:
        max_in_line = 8
        count_lines = int(math.ceil(float(count) / max_in_line))
        count_in_line = int(math.ceil(float(count) / count_lines))

        for i in range(count_lines):
            keyboard.append([]); callback.append([])
            for number in range(i*count_in_line + 1, min(i*count_in_line + max_in_line + 1, count + 1)):
                keyboard[i].append(number)
                if position != number:
                    callback[i].append("catalog_item {category_id} {position} {photo_message_id}".format(category_id=category_id, position=number, photo_message_id=photo_message_id))
                else:
                    callback[i].append("scroll {category_id} {position} {photo_message_id} 1".format(category_id=category_id, position=position, photo_message_id=photo_message_id))



    keyboard.append(["Добавить в корзину"])
    callback.append(["basket add {category_id} {position}".format(category_id=category_id, position=position)])

    keyboard.append(["Открыть корзину"])
    callback.append(["basket open"])

    keyboard.append(["Открыть меню"])
    callback.append(["menu open"])

    return keyboard, callback

def genarate_basket_kb(user_id):
    keyboard = []; callback = []

    table = db_main.Table(tables.names_dict["basket"])
    data = table.select(["item_code", "item_count"], "user_id", user_id)
    table.close()

    keyboard.append(["Перейти к оплате"])
    callback.append(["choose_adress"])

    for item in data:
        item_code, item_count = item[0], item[1]
        if item_count > 0:
            keyboard.append(["#{item_code}".format(item_code=item_code)])
            callback.append(["show_naked_item {item_code}".format(item_code=item_code)])

            keyboard.append(["-1", "Удалить", "+1"])
            callback.append(["basket_set_item_count {user_id} {item_code} {item_count}".format(user_id=user_id, item_code=item_code, item_count=item_count-1),
                             "basket_set_item_count {user_id} {item_code} 0".format(user_id=user_id, item_code=item_code),
                             "basket_set_item_count {user_id} {item_code} {item_count}".format(user_id=user_id, item_code=item_code, item_count=item_count+1)])

    keyboard.append(["Очистить корзину"])
    callback.append(["basket_erase"])

    keyboard.append(["Перейти к оплате"])
    callback.append(["choose_adress"])

    return keyboard, callback

def generate_item_text(name, description, price):
    text = markdown.text(
        markdown.bold("{name}".format(name=name)),
        markdown.text("Цена: {price}".format(price=price)),
        sep='\n\n')
    return text

def generate_basket_text(user_id):

    table = db_main.Table(db_config.tables.basket)
    data = table.select(["item_name", "item_code", "item_price", "item_count"], "user_id", user_id)
    table.close()

    text = ""; sum = 0
    for item in data:
        item_name, item_code, item_price, item_count = item[0], item[1], item[2], item[3]
        if item_count > 0:
            line_1 = markdown.bold("Товар #{item_code} - {item_name}".format(
                item_code=item_code,
                item_name=item_name
            ))
            line_2 = "Стоимость: {item_price} * {item_count} = {cost}".format(
                item_price=item_price,
                item_count=item_count,
                cost=item_price*item_count
            )
            text += line_1 + "\n" + line_2 + "\n" + "\n"
            sum += item_price * item_count
    text += "Общий чек: {sum} тенге".format(sum=sum)
    return text

def basket_sum(user_id):
    table = db_main.Table(tables.names_dict["basket"])
    data = table.select(["item_price", "item_count"], "user_id", user_id)
    table.close()
    sum = 0
    for price, count in data:
        sum += price * count
    return sum


@dp.message_handler(commands=['start', 'help'], func=lambda message: (len(admins) == 0))
async def start_first_admin(message: types.Message):
    telegram_id = message.chat.id

    table = db_main.Table(tables.names_dict["admins"])
    table.insert("telegram_id", telegram_id)
    table.close()

    table = db_main.Table(tables.names_dict["texts"])
    table.insert(["title", "text"], ["managers_chat", telegram_id])
    table.close()
    
    update_constants()
    await start(message)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    table = db_main.Table(tables.names_dict["user_order"])
    data = table.select("user_id", "user_id", message.chat.id)
    if len(data) == 0:
        table.insert("user_id", message.chat.id)
    table.close()

    await bot.send_message(message.chat.id, "Рады приветствовать")
    await menu(message)

@dp.message_handler(commands=['chat_here'], func=lambda message: message.from_user.id == admins[0])
async def start_chat(message: types.Message):
    table = db_main.Table(tables.names_dict["texts"])
    table.update("title", "managers_chat", "text", message.chat.id)
    table.close()
    await bot.send_message(message.chat.id, "Приветствую, в данный чат будут приходить оплаченные заказы.")
    update_constants()

# @dp.message_handler(commands=['start', 'help'])
# async def cats(message: types.Message):
#     print("ok")
#     texts = db_main.Table(db_config.tables.texts)
#     text = texts.select("text", "title", "hello")[0][0]#.encode("utf8")
#     print(text)
#     # media2 = types.InputMediaPhoto("AgADAgADxKkxG39y2EmQegeY5TQrXSv89A4ABMMgmZnmPm3ugs4DAAEC")
#     media2 = types.InputMediaPhoto("AgADAgADXKoxG1OayEnRmdpY9FjRroFVXw8ABGrWYXKuOqcD17oAAgI")
#     media = types.MediaGroup()
#     media.attach_photo("AgADAgADXKoxG1OayEnRmdpY9FjRroFVXw8ABGrWYXKuOqcD17oAAgI", 'cat-cat-cat.')
#     # media.attach_photo("AgADAgADXKoxG1OayEnRmdpY9FjRroFVXw8ABGrWYXKuOqcD17oAAgI", 'cat-cat-cat.')
#     # media.attach_photo("AgADAgADXKoxG1OayEnRmdpY9FjRroFVXw8ABGrWYXKuOqcD17oAAgI", 'cat-cat-cat.')
#
#     a = await bot.send_media_group(message.chat.id, media=media)
#
#     print(a[0])
#     print(a[0].message_id)
#     # print(a[1])
#     # print(a[1].message_id)
#     print ("____")
#     for b in a:
#         print(b)
#     # await bot.send_photo(message.chat.id, file_id = "AgADAgADXKoxG1OayEnRmdpY9FjRroFVXw8ABGrWYXKuOqcD17oAAgI")
#     await bot.send_message(message.chat.id, text,  reply_markup=keyboard_main.inline([["10", "20", "30", "40", "50", "60", "70", "80", "90", "10", "20", "30",], ["Object #00002"], ["HIDE KEYBOARD"]]))
#     # await bot.send_message(message.chat.id, text,  reply_markup=keyboard_main.inline([["Object #00001"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"], ["Object #00002"], ["HIDE KEYBOARD"]]))
#     # await bot.delete_message(chat_id = message.chat.id, message_id = 1949)
#
#     print (message.chat.id)
#     # await bot.edit_message_media(media = media2, chat_id = message.chat.id, message_id = 1948)
#     # await bot.edit_message_media(media = media2, chat_id = message.chat.id, message_id = 2265)
#     await bot.edit_message_media(media = media2, chat_id = 385778185, message_id = 2314)

# @dp.message_handler(func=lambda message: message.text == "Object #00001")
# async def object_00001(message):
#     await bot.send_message(message.chat.id, "Object #00001", reply_markup = keyboard_main.inline(["callback #00001", "callback #00002"], ["callback new #00001", "callback new #00002"]))
#
# @dp.message_handler(func=lambda message: message.text == "Object #00002")
# async def object_00002(message):
#     await bot.send_message(message.chat.id, "Object #00002", reply_markup = keyboard_main.inline([["callback #00003", "callback #00004"], ["callback #00005"]]))
#
# @dp.message_handler(func=lambda message: message.text == "HIDE KEYBOARD")
# async def command_text_hi(message):
#     await bot.send_message(message.chat.id, "KEYBOARD HIDDEN", reply_markup = keyboard_main.remove())

# @dp.message_handler(commands=['file'])
# async def process_file_command(message: types.Message):
#     user_id = message.from_user.id
#     await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
#     await bot.send_document(user_id, "text",
#                             caption='Этот файл специально для тебя!')
#     with open('data/cats.jpg', 'rb') as photo:
#         await bot.send_photo(message.chat.id, photo, caption='Cats is here',
#                              reply_to_message_id=message.message_id)

@dp.message_handler(func=lambda message: message.text in categories)
async def categories(message: types.Message):
    #
    # global categories
    # global count_items


    await bot.send_message(message.chat.id, message.text)

    #
    table = db_main.Table(tables.names_dict["items"])
    category_id = categories.index(message.text) + 1
    item = table.select(["name", "description", "price", "photo_id"], ["category_id", "position"], [category_id, 1])[0]
    name, description, price, photo_id = item[0], item[1], item[2], item[3]
    table.close()

    media = types.MediaGroup()
    media.attach_photo(photo_id)
    photo_message = await bot.send_media_group(message.chat.id, media=media)
    photo_message_id = photo_message[0].message_id

    keyboard, callback = generate_kb(category_id, 1, photo_message_id)
    await bot.send_message(message.chat.id, generate_item_text(name, description, price), reply_markup=keyboard_main.inline(keyboard, callback))

@dp.message_handler(func=lambda message: "корзина" in message.text.lower())
async def basket_open_message(message: types.Message):

    table = db_main.Table(tables.names_dict["basket"])
    data = table.select("item_count", "user_id", message.chat.id)
    table.close()

    if len(data) > 0:
        keyboard, callback = genarate_basket_kb(message.chat.id)
        text = generate_basket_text(message.chat.id)
        await bot.send_message(message.chat.id, text, reply_markup=keyboard_main.inline(keyboard, callback))
    else:
        await bot.send_message(message.chat.id, "Корзина пуста")




# @dp.message_handler(content_types=ContentType.PHOTO | ContentType.DOCUMENT)
# async def audio_handler(message: types.Message):
#     await bot.send_message(message.chat.id, "PHOTO ok")
#     print(message)

#
@dp.callback_query_handler(lambda callback_query: "catalog_item" in callback_query.data)
async def show_item(callback: types.CallbackQuery, change_scroll = False, scroll = True):

    message = callback.message
    category_id, position, photo_message_id = int(callback.data.split()[1]), int(callback.data.split()[2]), int(callback.data.split()[3])

    table = db_main.Table(tables.names_dict["items"])
    item = table.select(["name", "description", "price", "photo_id"], ["category_id", "position"], [category_id, position])[0]
    name, description, price, photo_id = item[0], item[1], item[2], item[3]
    table.close()

    if change_scroll == False:
        media = types.InputMediaPhoto(photo_id)
        await bot.edit_message_media(chat_id=message.chat.id, message_id=photo_message_id, media=media)

    keyboard, callback = generate_kb(category_id, position, photo_message_id, scroll)
    if change_scroll == False:
        await bot.edit_message_text(chat_id = message.chat.id, message_id = message.message_id, text = generate_item_text(name, description, price),  reply_markup = keyboard_main.inline(keyboard, callback))
    else:
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard_main.inline(keyboard,callback))

@dp.callback_query_handler(lambda callback_query: "menu" in callback_query.data)
async def some_callback_handler(callback: types.CallbackQuery):
    await menu(callback.message)

@dp.callback_query_handler(lambda callback_query: "scroll" in callback_query.data)
async def change_scroll(callback: types.CallbackQuery):
    scroll = bool(int(callback.data.split()[4]))
    await show_item(callback, change_scroll = True, scroll = scroll)
    # await bot.send_message(callback.from_user.id, "CALLBACK: " + callback.data)

@dp.callback_query_handler(lambda callback_query: "basket add" in callback_query.data)
async def basket_add(callback: types.CallbackQuery):
    category_id, position = int(callback.data.split()[2]), int(callback.data.split()[3])
    message = callback.message

    table = db_main.Table(tables.names_dict["items"])
    item = table.select(["code", "name", "price"], ["category_id", "position"], [category_id, position])[0]
    item_code, item_name, item_price = item[0], item[1], item[2]
    table.close()

    table = db_main.Table(tables.names_dict["basket"])
    data = table.select("item_count", ["user_id", "item_code"], [message.chat.id, item_code])
    if len(data) > 0:
        item_count = data[0][0]
        table.update(["user_id", "item_code"], [message.chat.id, item_code], "item_count", item_count+1)
        await callback.answer("Количество данного товара в корзине: {item_count}".format(item_count=item_count+1))
    else:
        table.insert(["user_id", "item_code", "item_name", "item_count", "item_price"], [message.chat.id, item_code, item_name, 1, item_price])
        await callback.answer("Добавлено в корзину")
    table.close()


@dp.callback_query_handler(lambda callback_query: "basket open" in callback_query.data)
async def basket_open(callback: types.CallbackQuery):
    message = callback.message

    table = db_main.Table(tables.names_dict["basket"])
    data = table.select("item_count", "user_id", message.chat.id)
    table.close()

    if len(data) > 0:
        keyboard, callback = genarate_basket_kb(message.chat.id)
        text = generate_basket_text(message.chat.id)
        await bot.send_message(message.chat.id, text, reply_markup = keyboard_main.inline(keyboard, callback))
    else:
        await callback.answer("Корзина пуста")


@dp.callback_query_handler(lambda callback_query: "basket_set_item_count" in callback_query.data)
async def any_callback(callback: types.CallbackQuery):
    message = callback.message

    user_id, item_code, item_count = int(callback.data.split()[1]), int(callback.data.split()[2]), int(callback.data.split()[3])

    table = db_main.Table(tables.names_dict["basket"])

    if item_count > 0:
        table.update(["user_id", "item_code"], [user_id, item_code], "item_count", item_count)
        table.close()
        text = generate_basket_text(user_id)
        keyboard, callback = genarate_basket_kb(user_id)
        await bot.edit_message_text(text=text, chat_id=user_id, message_id=message.message_id, reply_markup = keyboard_main.inline(keyboard, callback))
    else:
        table.delete(["user_id", "item_code"], [user_id, item_code])
        basket_items = table.select("item_code", "user_id", user_id)
        if len(basket_items) > 0:
            text = generate_basket_text(user_id)
            keyboard, callback = genarate_basket_kb(user_id)
            await bot.edit_message_text(text=text, chat_id=user_id, message_id=message.message_id, reply_markup = keyboard_main.inline(keyboard, callback))
        else:
            await bot.edit_message_text(text="Корзина пуста", chat_id=user_id, message_id=message.message_id)
        table.close()

@dp.callback_query_handler(lambda callback_query: "basket_erase" in callback_query.data)
async def basket_erase(callback: types.CallbackQuery):
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id

    table = db_main.Table(tables.names_dict["basket"])
    table.delete("user_id", message.chat.id)
    table.close()

    await bot.edit_message_text(text="Корзина пуста", chat_id=user_id, message_id=message_id)


@dp.callback_query_handler(lambda callback_query: "show_naked_item" in callback_query.data)
async def any_callback(callback: types.CallbackQuery):
    item_code = int(callback.data.split()[1])
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id

    table = db_main.Table(tables.names_dict["items"])
    name, description, price, photo_id = table.select(["name", "description", "price", "photo_id"], "code", item_code)[0]
    table.close()

    media = types.MediaGroup()
    media.attach_photo(photo_id)
    await bot.send_media_group(user_id, media=media)

    text = generate_item_text(name, description, price)
    await bot.send_message(user_id, text)


@dp.callback_query_handler(lambda callback_query: "choose_adress" in callback_query.data)
async def any_callback(callback: types.CallbackQuery):
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id

    table = db_main.Table(tables.names_dict["delivery_adress"])
    adresses = table.select_all(["id", "delivery_adress"])
    table.close()

    keyboard, callback, text = [], [], ""

    for adress_id, adress in adresses:
        keyboard.append([adress])
        callback.append(["set_adress {adress_id}".format(adress_id = adress_id)])
        text += adress + "\n"
    keyboard.append(["Отмена"])
    callback.append(["cancel_adress"])

    await bot.send_message(user_id, text, reply_markup=keyboard_main.inline(keyboard, callback))

    # await bot.send_message(user_id, "Укажите адрес доставки:", reply_markup = keyboard_main.force_reply())


@dp.callback_query_handler(lambda callback_query: "cancel_adress" in callback_query.data)
async def any_callback(callback: types.CallbackQuery):
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    bot.edit_message_text(text = "Выбор адреса отменен", chat_id = user_id, message_id = message_id)

@dp.callback_query_handler(lambda callback_query: "set_adress" in callback_query.data)
async def any_callback(callback: types.CallbackQuery):
    adress_id = int(callback.data.split()[1])

    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    sum = basket_sum(user_id)

    table = db_main.Table(tables.names_dict["user_order"])
    table.update("user_id", user_id, ["adress_id", "sum"], [adress_id, sum])
    table.close()

    await bot.edit_message_text(text = "Адрес выбран", chat_id = user_id, message_id = message_id)


    text = "Совершите перевод на кошелек QIWI, при оплате обязательно укажите комментарий, приведенный ниже."
    text += "\nНомер: {number}\nСумма: {sum}\nКомментарий: {comment}".format(
        number = texts["number"],
        sum = sum,
        comment = user_id
    )
    link = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={number}&amountInteger={sum}&amountFraction=0&currency=398&extra%5B%27comment%27%5D={comment}&currency=643&blocked[0]=sum&blocked[1]=account&blocked[2]=comment".format(
        number = texts["number"],
        sum = sum,
        comment = user_id
    )
    await bot.send_message(user_id, text, reply_markup = keyboard_main.url("Перейти в QIWI", url = link))
    await bot.send_message(user_id, "После оплаты нажмите кнопку проверки", reply_markup = keyboard_main.inline("Проверка оплаты", "check_payment"))


@dp.callback_query_handler(lambda callback_query: "check_payment" in callback_query.data)
async def any_callback(callback: types.CallbackQuery):
    message = callback.message
    user_id = message.chat.id

    table = db_main.Table(tables.names_dict["user_orders"])
    orders = table.select(["order_code", "delivery_adress"], ["user_id", "checked"], [user_id, 0])
    table.update("user_id", user_id, "checked", 1)
    table.close()

    for order, delivery_adress in orders:
        text = "Номер заказа: {order}\nАдрес доставки: {delivery_adress}\n\n".format(
            order = order,
            delivery_adress = delivery_adress
        )
        table = db_main.Table(tables.names_dict["orders"])
        order_items = table.select(["item_code", "item_name", "item_price", "item_count"], "order_code", order)
        table.close()

        for item_code, item_name, item_price, item_count in order_items:
            table = db_main.Table(tables.names_dict["items"])
            description = table.select("description", "code", item_code)[0][0]
            table.close()
            text += "Товар #{item_code}\n{item_name}\nКоличество: {item_count}\nОписание: {description}".format(
                item_code = item_code,
                item_name = item_name,
                item_count = item_count,
                description = description
            )
        await bot.send_message(user_id, text)
        await bot.send_message(user_id, "ЗАКАЗ ОПЛАЧЕН")
        await bot.send_message(int(texts["managers_chat"]), text)


@dp.message_handler(func=lambda message: "Добавить категорию"  in message.text and message.chat.id in admins)
async def categories(message: types.Message):
    user_id = message.chat.id
    keyboard = keyboard_main.force_reply()
    await bot.send_message(user_id, texts["new_category"], reply_markup=keyboard)

@dp.message_handler(func=lambda message: "Добавить товар"  in message.text and message.chat.id in admins)
async def categories(message: types.Message):
    user_id = message.chat.id
    keyboard = keyboard_main.force_reply()
    await bot.send_message(user_id, texts["new_item_name"], reply_markup=keyboard)

@dp.message_handler(func=lambda message: "Добавить адрес"  in message.text and message.chat.id in admins)
async def categories(message: types.Message):
    user_id = message.chat.id
    keyboard = keyboard_main.force_reply()
    await bot.send_message(user_id, texts["new_adress"], reply_markup=keyboard)

@dp.message_handler(func=lambda message: "Номер QIWI"  in message.text and message.chat.id in admins)
async def categories(message: types.Message):
    user_id = message.chat.id
    keyboard = keyboard_main.force_reply()
    await bot.send_message(user_id, texts["number_qiwi"], reply_markup=keyboard)
    pass # перезапуск qiwi-модуля

@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_category"] in message.reply_to_message.text)
async def add_category(message: types.Message):
    table = db_main.Table(tables.names_dict["categories"])
    # !!!! count_items in categories
    table.insert("name", message.text)
    table.close()
    update_constants()
    await bot.send_message(message.chat.id, "КАТЕГОРИЯ ДОБАВЛЕНА")
    await menu(message)

@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_adress"] in message.reply_to_message.text)
async def new_adress(message: types.Message):
    table = db_main.Table(tables.names_dict["delivery_adress"])
    table.insert("delivery_adress", message.text)
    table.close()

    await bot.send_message(message.chat.id, "АДРЕС ДОБАВЛЕН")
    await menu(message)

@dp.message_handler(func=lambda message: message.reply_to_message and texts["number_qiwi"] in message.reply_to_message.text)
async def number_qiwi(message: types.Message):

    table = db_main.Table(tables.names_dict["texts"])
    table.update("title", "number", "text", message.text)
    table.close()

    update_constants()

    user_id = message.chat.id
    keyboard = keyboard_main.force_reply()
    await bot.send_message(user_id, texts["token_qiwi"], reply_markup=keyboard)

@dp.message_handler(func=lambda message: message.reply_to_message and texts["token_qiwi"] in message.reply_to_message.text)
async def number_qiwi(message: types.Message):

    table = db_main.Table(tables.names_dict["texts"])
    table.update("title", "qiwi_api_access_token", "text", message.text)
    table.close()

    update_constants()

    await bot.send_message(message.chat.id, "Номер QIWI ДОБАВЛЕН")
    await menu(message)

@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_item_name"] in message.reply_to_message.text)
async def new_item_name(message: types.Message):
    table = db_main.Table(tables.names_dict["items"])
    table.insert("name", message.text)
    table.close()

    await bot.send_message(message.chat.id, texts["new_item_description"], reply_markup=keyboard_main.force_reply())

@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_item_description"] in message.reply_to_message.text)
async def new_item_description(message: types.Message):
    table = db_main.Table(tables.names_dict["items"])
    data = table.select_by_max("id", "id")
    id = data[0][0]
    table.update("id", id, "description", message.text)
    table.close()

    await bot.send_message(message.chat.id, texts["new_item_code"], reply_markup=keyboard_main.force_reply())

@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_item_code"] in message.reply_to_message.text)
async def new_item_code(message: types.Message):
    table = db_main.Table(tables.names_dict["items"])
    data = table.select_by_max("id", "id")
    id = data[0][0]
    table.update("id", id, "code", message.text)
    table.close()

    await bot.send_message(message.chat.id, texts["new_item_price"], reply_markup=keyboard_main.force_reply())


@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_item_price"] in message.reply_to_message.text)
async def new_item_price(message: types.Message):
    table = db_main.Table(tables.names_dict["items"])
    data = table.select_by_max("id", "id")
    id = data[0][0]
    table.update("id", id, "price", message.text)
    table.close()

    await bot.send_message(message.chat.id, texts["new_item_photo"], reply_markup=keyboard_main.force_reply())


@dp.message_handler(content_types=ContentType.PHOTO, func=lambda message: message.reply_to_message and texts["new_item_photo"] in message.reply_to_message.text)
async def new_item_category(message: types.Message):
    table = db_main.Table(tables.names_dict["items"])
    data = table.select_by_max("id", "id")
    id = data[0][0]
    table.update("id", id, "photo_id", message.photo[0].file_id)
    table.close()

    # print (message.photo[0].file_id)
    # print (message.reply_to_message)
    # print ("---\nphoooto\n---")
    #
    # media = types.MediaGroup()
    # for photo in message.photo:
    #     media.attach_photo(photo.file_id)
    # await bot.send_media_group(message.chat.id, media=media)
    text_categories = ""
    for i, category in enumerate(categories):
        text_categories += "\n{i}. {category}".format(i = i+1, category = category)
    await bot.send_message(message.chat.id, texts["new_item_category"] + text_categories, reply_markup=keyboard_main.force_reply())


@dp.message_handler(func=lambda message: message.reply_to_message and texts["new_item_category"] in message.reply_to_message.text)
async def new_item_price(message: types.Message):
    category_name = categories[int(message.text) - 1]
    table = db_main.Table(tables.names_dict["categories"])
    data = table.select(["id", "count_items"], "name", category_name)[0]
    category_id, count_items = data[0], data[1]
    table.update("id", category_id, "count_items", count_items+1)
    table.close()

    table = db_main.Table(tables.names_dict["items"])
    id = table.select_by_max("id", "id")[0][0]
    table.update("id", id, ["category_id", "position"], [category_id, count_items+1])
    table.close()

    update_constants()
    await bot.send_message(message.chat.id, "ТОВАР ДОБАВЛЕН")
    await menu(message)

@dp.message_handler(func=lambda message: message.chat.id == admins[0] and ("Добавить менеджера" in message.text or "Чат менеджеров" in message.text))
async def add_admin(message: types.Message):
    global forward_target
    if "Добавить менеджера" in message.text:
        await bot.send_message(message.chat.id, "Для добавления менеджера просто перешлите его сообщение")
    if "Чат менеджеров" in message.text:
        await bot.send_message(message.chat.id, "Добавьте бота в чат с менеджерами и запустите команду /chat_here")

@dp.message_handler(func=lambda message: message.forward_from and message.chat.id == admins[0], content_types = ContentType.TEXT | ContentType.AUDIO)
async def add_admin(message: types.Message):
    user_id = message.forward_from.id
    table = db_main.Table(tables.names_dict["admins"])
    table.insert("telegram_id", user_id)
    table.close()
    await bot.send_message(message.chat.id, "МЕНЕДЖЕР ДОБАВЛЕН")

    update_constants()


@dp.message_handler(func=lambda message: "менеджер" in message.text.lower())
async def manager_question(message: types.Message):
    await bot.send_message(message.chat.id, texts["manager_question"], reply_markup = keyboard_main.force_reply())


@dp.message_handler(func=lambda message: message.reply_to_message and texts["manager_question"] in message.reply_to_message.text, content_types = ContentType.TEXT | ContentType.AUDIO)
async def manager_question(message: types.Message):
    await message.forward(int(texts["managers_chat"]))
    await bot.send_message(message.chat.id, "Ваш запрос отправлен")
    await menu(message)

@dp.message_handler()
async def menu(message: types.Message):
    user_id = message.chat.id

    global categories
    menu = categories.copy()
    menu.append(["Корзина","Заказы","Менеджер"])

    if user_id in admins:
        menu.append(["Добавить категорию"])
        menu.append(["Добавить товар"])
        if user_id == admins[0]:
            menu.append(["Добавить менеджера", "Чат менеджеров"])
            menu.append(["Добавить адрес", "Номер QIWI"])

    print (message)
    print (message.reply_to_message)
    # print (message.reply_message)
    text = markdown.text(markdown.bold("hello"))
    # texts["menu"]
    await bot.send_message(message.chat.id, texts["menu"], reply_markup = keyboard_main.reply(menu, one_time_keyboard = True))


@dp.callback_query_handler(lambda callback_query: True)
async def any_callback(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "CALLBACK: " + callback.data)

async def good_order(user_id):

    table = db_main.Table(tables.names_dict["order"])
    adress_id = table.select("adress_id", "user_id", user_id)[0][0]
    table.update("user_id", user_id, "sum", 0)
    table.close()

    table = db_main.Table(tables.names_dict["delivery_adress"])
    delivery_adress = table.select("delivery_adress", "id", adress_id)[0][0]
    table.close()

    await bot.send_message(user_id, "{delivery_adress}\nID пользователя: {user_id}\n\n".format(delivery_adress=delivery_adress, user_id=user_id) + generate_basket_text(user_id))
    await bot.send_message(user_id, "ЗАКАЗ ОПЛАЧЕН")
    await bot.send_message(int(texts["managers_chat"]), "{delivery_adress}\nID пользователя: {user_id}\n\n".format(delivery_adress=delivery_adress, user_id=user_id) + generate_basket_text(user_id))

    table = db_main.Table(tables.names_dict["basket"])
    table.delete("user_id", user_id)
    table.close()



def update_constants():
    # --- --- ---
    global categories
    global count_items
    table = db_main.Table("categories")
    data = table.select_all(["name", "count_items"])
    table.close()

    categories = [category[0] for category in data]
    count_items = [category[1] for category in data]

    # --- --- ---
    global texts
    table = db_main.Table("texts")
    data = table.select_all(["title", "text"])
    table.close()

    texts = dict(data)

    # --- --- ---
    global admins
    table = db_main.Table("admins")
    data = table.select_all("telegram_id")
    table.close()
    admins = [category[0] for category in data]
    print (admins)

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def basket_to_orders(user_id):

    table = db_main.Table(tables.names_dict["user_order"])
    adress_id = table.select("adress_id", "user_id", user_id)[0][0]
    table.update("user_id", user_id, "sum", 0)
    table.close()

    table = db_main.Table(tables.names_dict["delivery_adress"])
    delivery_adress = table.select("delivery_adress", "id", adress_id)[0][0]
    table.close()

    table = db_main.Table(tables.names_dict["basket"])
    basket = table.select(["item_code", "item_name", "item_price", "item_count"], "user_id", user_id)
    table.close()

    order = randomword(10)

    table = db_main.Table(tables.names_dict["user_orders"])
    table.insert(["user_id", "order_code", "delivery_adress"], [user_id, order, delivery_adress])
    table.close()

    table = db_main.Table(tables.names_dict["orders"])
    for item_code, item_name, item_price, item_count in basket:
        table.insert(["item_code", "item_name", "item_price", "item_count", "order_code"], [item_code, item_name, item_price, item_count, order])
    table.close()

    table = db_main.Table(tables.names_dict["basket"])
    table.delete("user_id", user_id)
    table.close()

def qiwi_update():
    global texts

    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + texts["qiwi_api_access_token"]
    parameters = {'rows': '10', 'operation': 'IN'}
    h = s.get(
        'https://edge.qiwi.com/payment-history/v1/persons/{qiwi_login}/payments'.format(qiwi_login=texts["number"]),
        params=parameters)
    # try:
    data = json.loads(h.text)
    lastTxnId = int(texts["lastTxnId"])

    if data["data"]:
        TxnId = data["data"][0]["txnId"]

        if TxnId > lastTxnId and lastTxnId != 0:
            print ("QIWI new transaction")
            for transaction in data["data"]:
                if transaction["txnId"] > lastTxnId:
                    if transaction["status"] == "SUCCESS" and transaction["sum"]["currency"] == 398: # !!!=====
                        if transaction["comment"].isdigit():
                            user_id = int(transaction["comment"])
                            sum = int(transaction["sum"]["amount"])
                            print (sum, user_id)
                            table = db_main.Table(tables.names_dict["user_order"])
                            data = table.select("sum", "user_id", user_id)
                            table.close()
                            if len(data) > 0:
                                necessary_sum = data[0][0]
                                if sum >= necessary_sum:
                                    basket_to_orders(user_id)


                else:
                    break
        if TxnId > lastTxnId or lastTxnId == 0:
            table = db_main.Table(tables.names_dict["texts"])
            table.update("title", "lastTxnId", "text", TxnId)
            table.close()
            update_constants()

        # except:
        #     print ("Problems in qiwi auth")

    threading.Timer(5, qiwi_update).start()

def test():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(good_order(385778185))
    # loop.close()



update_constants()


qiwi_update()
# test()

executor.start_polling(dp, skip_updates=True)
