import keyboard
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
import config

bot = Bot(token = config.telegram_token)
dp = Dispatcher(bot)

async def removeReplyKB(message: types.Message):
    service_message = await bot.send_message(message.chat.id, "service work", reply_markup = keyboard.removeReply())
    await bot.delete_message(service_message["chat"]["id"], service_message["message_id"])

@dp.message_handler(commands=['start', 'about'])
async def cats(message: types.Message):
    print("ok")
    await bot.send_message(message.chat.id, "Get started!", reply_markup = keyboard.get(kb_id = 9))


@dp.message_handler()
async def echo(message: types.Message):
    await removeReplyKB(message)
    await bot.send_message(message.chat.id, message.text)
    # await bot.send_message(message.chat.id, message.text, reply_markup = keyboard.removeReply())
    # await bot.send_message(message.chat.id, message.text, reply_markup = keyboard.get(kb_id = 9))


executor.start_polling(dp, skip_updates=True)