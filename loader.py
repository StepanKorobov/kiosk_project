from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from database.models import create_tables
from database.database import Base, engine

Base.metadata.create_all(bind=engine)
storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
