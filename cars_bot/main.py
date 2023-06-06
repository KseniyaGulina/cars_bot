#!venv/bin/python
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import cars_bot.config as config

loop = asyncio.new_event_loop()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

def main():
    from cars_bot.handlers import dp

    executor.start_polling(dp)
