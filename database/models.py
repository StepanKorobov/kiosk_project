from database.database import Base, get_session, User, Kiosk, KioskProduct, CartItem, Order, OrderItem, \
    OrderStatus, Product
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from datetime import datetime


def create_tables():
    """Функция создания БД"""

    with get_session() as session:
        Base.metadata.create_all(bind=session)


def add_user(username, telegram_id):
    with get_session() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(username=username, telegram_id=telegram_id, blocked=False)
            session.add(user)
            session.commit()


# def get_all_kiosks_address():
#     with get_session() as session:
#         kiosks = session.query(Kiosks).all()
#         return kiosks

def create_or_get_user(db: Session, telegram_id: int, username: str = None):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# def init_test_data():
#     db = get_db()
#     try:
#         # Тестовый юзер
#         create_or_get_user(db, 123456789, "testuser")
#
#         # Тестовый ларек
#         kiosk = Kiosk(id=1, address="ул. Ленина 10", lat=55.75, lon=37.61)
#         db.merge(kiosk)
#
#         # Тестовые товары
#         kp1 = KioskProduct(id=1, kiosk_id=1, product_id=1, count=10, price=50.0)
#         kp2 = KioskProduct(id=2, kiosk_id=1, product_id=2, count=5, price=30.0)
#         db.merge(kp1)
#         db.merge(kp2)
#         db.commit()
#     finally:
#         db.close()


def get_all_kiosks(db: Session):
    with get_session() as session:
        result = session.query(Kiosk).all()
        return result


def get_kiosk_products(db: Session, kiosk_id: int):
    with get_session() as session:
        result = session.query(KioskProduct).filter(
            KioskProduct.kiosk_id == kiosk_id
        ).options(joinedload(KioskProduct.product)).all()
        return result


def get_user_cart(db: Session, user_id: int):
    # with get_session() as session:
    #     result = session.query(CartItem).filter(
    #         CartItem.user_id == user_id
    #     ).options(
    #         joinedload(CartItem.kiosk_product).joinedload(KioskProduct.product)
    #     ).all()
    #     return result
    with get_session() as session:
        cart_items = session.query(CartItem).filter(CartItem.user_id == user_id).all()
        for item in cart_items:
            # Принудительно подгружаем kiosk_product + product
            item.kiosk_product = session.query(KioskProduct).get(item.kiosk_product_id)
            if item.kiosk_product:
                item.kiosk_product.product = session.query(Product).get(item.kiosk_product.product_id)

        return cart_items


def add_to_cart(db: Session, user_id: int, kiosk_product_id: int):
    with get_session() as session:
        cart_item = session.query(CartItem).filter(
            and_(CartItem.user_id == user_id, CartItem.kiosk_product_id == kiosk_product_id)
        ).first()

        if cart_item:
            cart_item.count += 1
        else:
            kp = session.query(KioskProduct).get(kiosk_product_id)
            cart_item = CartItem(
                user_id=user_id,
                kiosk_product_id=kiosk_product_id,
                count=1
            )
            session.add(cart_item)
        session.commit()
        session.refresh(cart_item)
        return cart_item


def create_order_from_cart(db: Session, user_id: int, kiosk_id: int, payment_type: str):
    with get_session() as session:
        cart_items = get_user_cart(db, user_id)
        if not cart_items:
            return None

        total_cost = sum(item.count * item.kiosk_product.price for item in cart_items)

        order = Order(
            user_id=user_id,
            kiosk_id=kiosk_id,
            cost=total_cost,
            status=OrderStatus.PAID if payment_type == "now" else OrderStatus.NEW
        )
        session.add(order)
        # session.commit()
        # session.refresh(order)

        # Создаём элементы заказа
        for cart_item in cart_items:
            oi = OrderItem(
                order_id=order.id,
                kiosk_product_id=cart_item.kiosk_product_id,
                count=cart_item.count,
                price=cart_item.kiosk_product.price
            )
            session.add(oi)

        # Очищаем корзину
        session.query(CartItem).filter(CartItem.user_id == user_id).delete()
        session.commit()

        fresh_order = session.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.id.desc()).first()

        return fresh_order


def get_user_orders(db: Session, user_id: int, limit=5):
    with get_session() as session:
        result = db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).limit(limit).all()
        return result
