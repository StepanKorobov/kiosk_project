from telebot.types import Message

from loader import bot
from database.models import add_user
from keyboards.inline.inline import main_menu


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    username = message.from_user.username
    telegram_id = message.from_user.id
    add_user(telegram_id, username)

    bot.send_message(
        message.chat.id,
        "🍔 Добро пожаловать в бот ларьков!\nВыбери действие:",
        reply_markup=main_menu()
    )


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def show_all_kiosks(call):
    bot.edit_message_text(
        "🍔 Добро пожаловать в бот ларьков!\nВыбери действие:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=main_menu()
    )
