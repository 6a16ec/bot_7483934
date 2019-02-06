import asyncio
import logging
import config

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor, markdown


API_TOKEN = config.telegram_token

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


@dp.message_handler()
async def check_language(message: types.Message):
    name = "test"
    text = markdown.text(
        markdown.bold("{name}".format(name=name)),
        markdown.text(' 🔸', markdown.bold('Code:'), markdown.italic("RUS")),
        sep='\n')
    await message.reply(text)


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)