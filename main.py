#!venv/bin/python
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

loop = asyncio.new_event_loop()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

# logging.basicConfig(level=logging.INFO)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp)
