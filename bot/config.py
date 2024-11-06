from os import getenv
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.utils.postgres.repository.database import Database

load_dotenv()


BOT_TOKEN = getenv("BOT_TOKEN")
DB_URL = "postgresql://test:test@localhost/test"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
database = Database(DB_URL)