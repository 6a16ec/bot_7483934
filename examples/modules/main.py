from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
import config, keyboard

bot = Bot(token=config.telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'about'])
async def cats(message: types.Message):
    print("ok")
    await bot.send_message(message.chat.id, "И тебе привет!", reply_markup=keyboard.reply([["create task"], ["tasks"]]))


@dp.message_handler(func=lambda message: message.text == "create task")
async def command_text_hi(message):
    await bot.send_message(message.chat.id, "Creating...", reply_markup = keyboard.remove())


@dp.message_handler(func=lambda message: message.text == "tasks")
async def command_text_hi(message):
    await bot.send_message(message.chat.id, "Watching...", reply_markup = keyboard.remove())


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, "XUYNYA: " + message.text)


@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    print(callback_query)


executor.start_polling(dp, skip_updates=True)
