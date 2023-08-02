from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

load_dotenv()
token = os.getenv("TOKEN")

bot = Bot(token=token)
dispatcher = Dispatcher(bot, storage=storage)
