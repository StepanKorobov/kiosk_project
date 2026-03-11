from loader import bot
from database.models import get_user_orders, create_order_from_cart, get_session
from keyboards.inline.inline import payment_keyboard, order_status_keyboard


@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def checkout(call):
    bot.edit_message_text(
        "💳 Выбери способ оплаты:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=payment_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def process_payment(call):
    payment_type = call.data.split('_')[1]
    with get_session() as db:
        order = create_order_from_cart(db, call.from_user.id, 1, payment_type)  # kiosk_id=1
        if order:
            status_text = "✅ Оплачен" if payment_type == "now" else "⏳ Ожидает оплаты"
            text = f"🎉 Заказ #{order.id} создан!\n{status_text}\n💰 {order.cost}₽"
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=order_status_keyboard(order.id)
            )
        else:
            bot.answer_callback_query(call.id, "❌ Корзина пуста")


@bot.callback_query_handler(func=lambda call: call.data == "history")
def show_history(call):
    with get_session() as db:
        orders = get_user_orders(db, call.from_user.id)
        if not orders:
            bot.edit_message_text("📋 История заказов пуста", call.message.chat.id, call.message.message_id)
            return

        text = "📋 Последние заказы:\n\n"
        for order in orders:
            status_emojis = {
                'new': '⏳', 'paid': '✅', 'delivery': '🚚', 'done': '🎉', 'cancelled': '❌'
            }
            text += f"{status_emojis.get(order.status.value, '➤')} Заказ #{order.id} - {order.status.name.title()}\n"

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
