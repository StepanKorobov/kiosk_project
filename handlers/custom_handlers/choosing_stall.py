from telebot.types import Message

from loader import bot
from states.order import Order
from keyboards.inline.choosing_stall import choosing_stall_button


@bot.message_handler(commands=["choosing_stall"])
def choosing_stall(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Выберете точку:", reply_markup=choosing_stall_button())
