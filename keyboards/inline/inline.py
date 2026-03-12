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


def category_keyboard(category, kiosk_id):
    kb = InlineKeyboardMarkup()
    for i_category in category:
        kb.row(InlineKeyboardButton(
            f"{i_category.name}",
            callback_data=f"kiosks_{kiosk_id}_{i_category.id}"
        ))
    kb.row(InlineKeyboardButton("🏪 Ларьки", callback_data="all_kiosks"),
           InlineKeyboardButton("🛒 Корзина", callback_data=f"cart_{kiosk_id}"))
    # kb.row(InlineKeyboardButton("🛒 Корзина", callback_data=f"cart_{kiosk_id}"))
    kb.row(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    return kb


def assortment_keyboard(products, kiosk_id):
    kb = InlineKeyboardMarkup()
    for product in products:
        kb.row(InlineKeyboardButton(
            f"➕ {product.product.name} ({product.count}) {product.price}₽",
            callback_data=f"add_{product.id}"
        ))
    kb.row(InlineKeyboardButton("🛒 Корзина", callback_data=f"cart_{kiosk_id}"),
           InlineKeyboardButton("📂 Категории", callback_data=f"kiosk_{kiosk_id}"))
    kb.row(InlineKeyboardButton("🏪 Ларьки", callback_data="all_kiosks"),
           InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    return kb


def cart_keyboard(kiosk_id=0):
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout"))
    kb.row(InlineKeyboardButton("📂 Категории", callback_data=f"kiosk_{kiosk_id}"))
    kb.row(InlineKeyboardButton("🧹 Очистить корзину", callback_data=f"clear_cart_{kiosk_id}"))
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
    kb.row(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    return kb


def back_menu_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    return kb
