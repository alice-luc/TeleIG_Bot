from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.db_api.sqlite import Database
import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()  # requires the better way to store data on deploying
dp = Dispatcher(bot, storage=storage)
db = Database()
