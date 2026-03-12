from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from database.models import get_all_kiosks, get_kiosk_products, get_session
from keyboards.inline.inline import kiosks_keyboard, assortment_keyboard


@bot.callback_query_handler(func=lambda call: call.data == "all_kiosks")
def show_all_kiosks(call):
    with get_session() as db:
        kiosks = get_all_kiosks(db)
        bot.edit_message_text(
            "📋 Выбери ларек:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=kiosks_keyboard(kiosks)
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('kiosk_'))
def show_assortment(call):
    kiosk_id = int(call.data.split('_')[1])
    with get_session() as session:
        products = get_kiosk_products(session, kiosk_id)
        text = f"🍔 Ассортимент ларька #{kiosk_id}:\n\n"
        for p in products:
            text += f"• {p.product.name} - {p.price}₽ (осталось: {p.count})\n"

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=assortment_keyboard(products, kiosk_id)
        )


# @bot.message_handler(content_types=['location'])
@bot.callback_query_handler(func=lambda call: call.data == "nearest")
def handle_location(call):
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("🏪 ул. Ленина 10 (ближайший)", callback_data="kiosk_1"))
    bot.edit_message_text("📍 Ближайший ларек найден:", call.message.chat.id, call.message.message_id, reply_markup=kb)
