import asyncio
import threading

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import telegram_token
import keyboard
import users


permissions = users.access()
bot = Bot(token = telegram_token)
dp = Dispatcher(bot)

# handler audio-vedeo-photo (!!!)
@dp.message_handler(func=lambda message: message.chat.id != message.from_user.id)
async def any_chat(message: types.Message):
    chat_id, message_id = message.chat.id, message.message_id
    await bot.send_message(chat_id, "Сорян, я работаю только в ЛС. Жду там.")

@dp.message_handler(func=lambda message: len(permissions.owners) == 0)
async def owner(message: types.Message):
    user_id, message_id = message.from_user.id, message.message_id
    permissions.set_owner(user_id)
    await bot.send_message(user_id, "Вы владелец этого бота! Добро пожаловать!")

@dp.message_handler(func=lambda message: message.forward_from and permissions.user(message.chat.id)["add_employee"])
async def set_employee(message: types.Message):
    user_id, message_id = message.chat.id, message.message_id
    user_permissions = permissions.user(user_id)

    buttons, callback = [], []
    if user_permissions["add_admin"]:
        buttons.append(["Назначить администратором"])
        callback.append(["set_permissions_admin"])
    if user_permissions["add_manager"]:
        buttons.append("Назначить менеджером")
        callback.append(["set_permissions_manager"])
    if user_permissions["add_moderator"]:
        buttons.append(["Назначить модератором"])
        callback.append(["set_permissions_moderator"])

    await message.reply("Какие права дать данному пользователю?", reply_markup = keyboard.inline(buttons, callback))

@dp.message_handler(func=lambda message: message.chat.id in permissions.privileged_users)
async def privileged_people_main(message: types.Message):
    user_id, message_id = message.chat.id, message.message_id

    user_permissions = permissions.user(message.chat.id)
    button, callback = [], []

    if user_permissions["add_category"]:
        button.append(["Добавить категорию"])
        callback.append(["add_category"])
    if user_permissions["add_subcategory"]:
        button.append(["Добавить подкатегорию"])
        callback.append(["add_subcategory"])
    if user_permissions["add_item"]:
        button.append(["Добавить товар"])
        callback.append(["add_item"])
    if user_permissions["add_employee"]:
        button.append(["Добавление персонала"])
        callback.append(["add_employee"])
        button.append(["Удаление персонала"])
        callback.append(["delete_employee"])

    await bot.send_message(user_id, "Выберите действие", reply_markup = keyboard.inline(button, callback))
#
@dp.callback_query_handler(lambda callback_query: "add_employee" in callback_query.data)
async def adding_worker_info(callback: types.CallbackQuery):
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    await bot.send_message(user_id, "Для присваивания привелегий перешлите сообщение пользователя")
    await callback.answer(show_alert = False)

@dp.callback_query_handler(lambda callback_query: "set_permissions" in callback_query.data)
async def adding_worker_info(callback: types.CallbackQuery):
    await callback.answer(show_alert = False)

    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    employee_id = message.reply_to_message.forward_from.id

    text = ""
    if "set_permissions_admin" in callback.data:
        permissions.set_admin(employee_id)
        text = "Данному пользователю предоставлены права администратора"
    if "set_permissions_manager" in callback.data:
        permissions.set_manager(employee_id, user_id)
        text = "Данному пользователю предоставлены права менеджера"
    if "set_permissions_moderator" in callback.data:
        permissions.set_moderator(employee_id)
        text = "Данному пользователю предоставлены права модератора"

    await bot.edit_message_text(text=text, chat_id=user_id, message_id=message_id)
# !!!

@dp.callback_query_handler()
async def any_callback(callback: types.CallbackQuery):
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    await bot.send_message(user_id, "callback: " + callback.data)

@dp.message_handler()
async def any_message(message: types.Message):
    user_id, message_id = message.chat.id, message.message_id
    await bot.send_message(user_id, message.text)

# @dp.message_handler(commands=['start'], func=lambda message: message.chat.id == message.from_user.id)
# async def HelloWorld(message: types.Message):
#     user_id, message_id = message.from_user.id, message.message_id
#     await bot.send_message(user_id, "{user_id} {message_id}".format(user_id=user_id, message_id=message_id))
#     print (message)

#
# @dp.message_handler(commands=['start', 'help'], func=lambda message: (len(admins) == 0))
# async def start_first_admin(message: types.Message):
#     telegram_id = message.chat.id
#
#     table = db_main.Table(tables.names_dict["admins"])
#     table.insert("telegram_id", telegram_id)
#     table.close()
#
#     table = db_main.Table(tables.names_dict["texts"])
#     table.insert(["title", "text"], ["managers_chat", telegram_id])
#     table.close()
#
#     update_constants()
#     await
#     start(message)
# async def repeater():
#     try:
#         await bot.send_message(385778185, "repeater")
#     except:
#         print ("Не судьба")
#     await threading.Timer(5, repeater).start()
#
# repeater()
executor.start_polling(dp, skip_updates=True)