from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🗺️ Ближайший", callback_data="nearest"),
        InlineKeyboardButton("📋 Все ларьки", callback_data="all_kiosks")
    )
    kb.row(InlineKeyboardButton("🛒 Корзина", callback_data="cart"))
    kb.row(InlineKeyboardButton("📋 История", callback_data="history"))
    return kb

def kiosks_keyboard(kiosks):
    kb = InlineKeyboardMarkup()
    for kiosk in kiosks:
        kb.row(InlineKeyboardButton(f"🏪 {kiosk.address}", callback_data=f"kiosk_{kiosk.id}"))
    kb.row(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    return kb

def assortment_keyboard(products):
    kb = InlineKeyboardMarkup()
    for product in products:
        kb.row(InlineKeyboardButton(
            f"➕ {product.product.name} ({product.count}) {product.price}₽",
            callback_data=f"add_{product.id}"
        ))
    kb.row(InlineKeyboardButton("🛒 Корзина", callback_data="cart"))
    kb.row(InlineKeyboardButton("🔙 Ларьки", callback_data="all_kiosks"))
    return kb

def cart_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout"))
    kb.row(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    return kb

def payment_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("💳 Оплатить сейчас", callback_data="pay_now"))
    kb.row(InlineKeyboardButton("💰 Оплатить в ларьке", callback_data="pay_later"))
    kb.row(InlineKeyboardButton("🔙 Корзина", callback_data="cart"))
    return kb

def order_status_keyboard(order_id: int):
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("🔄 Обновить статус", callback_data=f"status_{order_id}"))
    kb.row(InlineKeyboardButton("📋 История заказов", callback_data="history"))
    return kb
