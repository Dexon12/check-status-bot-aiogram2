import dotenv
import os
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

dotenv.load_dotenv('.env')
bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')
storage = MemoryStorage()
