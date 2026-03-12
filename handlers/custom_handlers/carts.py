from loader import bot
from database.models import get_user_cart, add_to_cart, get_user_cart_with_kiosk, delete_user_catt_with_kiosk, \
    get_session
from keyboards.inline.inline import cart_keyboard, payment_keyboard, main_menu


@bot.callback_query_handler(func=lambda call: call.data.startswith("clear_cart_"))
def clear_cart_with_kiosk(call):
    kiosk_id = int(call.data.split("_")[2])
    with get_session() as db:
        delete_user_catt_with_kiosk(db, call.from_user.id, kiosk_id)
        bot.answer_callback_query(call.id, "🧹 Корзина очищена!")
        bot.edit_message_text(
            "🍔 Добро пожаловать в бот ларьков!\nВыбери действие:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("cart_"))
def show_cart_kiosk(call):
    kiosk_id = int(call.data.split("_")[1])
    with get_session() as db:
        cart_items = get_user_cart_with_kiosk(db, call.from_user.id, kiosk_id)
        if not cart_items:
            bot.edit_message_text("🛒 Корзина пуста", call.message.chat.id, call.message.message_id)
            return

        text = "🛒 Корзина:\n\n"
        total = 0
        for item in cart_items:
            price = item.count * item.kiosk_product.price
            total += price
            text += f"• {item.kiosk_product.product.name} x{item.count} = {price}₽\n"
        text += f"\n💰 Итого: {total}₽"

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cart_keyboard(kiosk_id))


@bot.callback_query_handler(func=lambda call: call.data == "cart")
def show_cart(call):
    with get_session() as db:
        cart_items = get_user_cart(db, call.from_user.id)
        if not cart_items:
            bot.edit_message_text("🛒 Корзина пуста", call.message.chat.id, call.message.message_id)
            return

        text = "🛒 Корзина:\n\n"
        total = 0
        for item in cart_items:
            price = item.count * item.kiosk_product.price
            total += price
            text += f"• {item.kiosk_product.product.name} x{item.count} = {price}₽\n"
        text += f"\n💰 Итого: {total}₽"

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cart_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def handle_add_to_cart(call):
    product_id = int(call.data.split('_')[1])
    with get_session() as db:
        add_to_cart(db, call.from_user.id, product_id)
        bot.answer_callback_query(call.id, "✅ Добавлено в корзину!")
