import asyncio

from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
import config, keyboard

from db_module import db_main, db_config

bot = Bot(token=config.telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def cats(message: types.Message):
    print("ok")
    texts = db_main.Table(db_config.tables.texts)
    text = texts.insert("text", "title", "hello")
    await bot.send_message(message.chat.id, text, reply_markup=keyboard.reply([["Object #00001"], ["Object #00002"], ["HIDE KEYBOARD"]]))


@dp.message_handler(func=lambda message: message.text == "Object #00001")
async def object_00001(message):
    await bot.send_message(message.chat.id, "Object #00001", reply_markup = keyboard.inline(["callback #00001", "callback #00002"], ["callback new #00001", "callback new #00002"]))

@dp.message_handler(func=lambda message: message.text == "Object #00002")
async def object_00002(message):
    await bot.send_message(message.chat.id, "Object #00002", reply_markup = keyboard.inline([["callback #00003", "callback #00004"], ["callback #00005"]]))


@dp.message_handler(func=lambda message: message.text == "HIDE KEYBOARD")
async def command_text_hi(message):
    await bot.send_message(message.chat.id, "KEYBOARD HIDDEN", reply_markup = keyboard.remove())

@dp.message_handler(commands=['file'])
async def process_file_command(message: types.Message):
    user_id = message.from_user.id
    await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
    await bot.send_document(user_id, "text",
                            caption='Этот файл специально для тебя!')
    with open('data/cats.jpg', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, caption='Cats is here',
                             reply_to_message_id=message.message_id)

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, "TEXT: " + message.text)

@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "CALLBACK: " + callback.data)



executor.start_polling(dp, skip_updates=True)
