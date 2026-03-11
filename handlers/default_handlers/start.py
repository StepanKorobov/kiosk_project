from telebot.types import Message

from loader import bot
from database.models import add_user


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    username = message.from_user.username
    telegram_id = message.from_user.id
    add_user(telegram_id, username)

    bot.reply_to(message, f"Добро пожаловать в бот по заказу продуктов для самовывоза.")
