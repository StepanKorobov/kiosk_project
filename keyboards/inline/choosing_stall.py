from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from database.models import get_all_kiosks_address


def choosing_stall_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    buttons_in_row = 2
    buttons_added = []

    buttons_added.append(InlineKeyboardButton(text="ddd", callback_data="ddd"))
    # print(get_all_kiosks_address())
    keyboard.add(*buttons_added)
    return keyboard
