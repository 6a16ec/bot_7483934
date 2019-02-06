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


@dp.message_handler(commands=['start', 'help'])
async def start_first_admin(message: types.Message):
    await bot.send_message(message.chat.id, "Приве")
