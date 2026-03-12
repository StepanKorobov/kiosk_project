from typing import List
from contextlib import contextmanager
from sqlalchemy import create_engine, Integer, String, Boolean, func, Float, DECIMAL, ForeignKey, Column, BigInteger, \
    DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase, Relationship, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from enum import Enum
from datetime import datetime

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    """Контекстный менеджер для получения сессии"""
    session = Session()
    try:
        yield session
    except Exception as exc:
        print(exc, type(exc))
        session.rollback()
    finally:
        session.close()


class Base(DeclarativeBase):
    pass


# class User(Base):
#     __tablename__ = "user"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     username: Mapped[str] = mapped_column(String, nullable=False)
#     telegram_id: Mapped[int] = mapped_column(String, nullable=False, unique=True)
#     blocked: Mapped[bool] = mapped_column(Boolean, default=False)
#
#     # kiosk_owner: Mapped[List["Kiosks"]] = Relationship(back_populates="owner")
#     # orders: Mapped[List["Orders"]] = Relationship(back_populates="user")
#
#
# class Kiosks(Base):
#     __tablename__ = "kiosks"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     address: Mapped[str] = mapped_column(String, nullable=False)
#     # lat: Mapped[float] = mapped_column(Float, nullable=True)
#     # lon: Mapped[float] = mapped_column(Float, nullable=True)
# #     owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
# #     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
# # #
# #     owner: Mapped[List["User"]] = Relationship(back_populates="kiosk_owner")
# #     orders: Mapped[List["Orders"]] = Relationship(back_populates="kiosks")
# #     stock: Mapped[List["KioskStock"]] = Relationship(back_populates="kiosk")
# #
# #
# # class Orders(Base):
# #     __tablename__ = "orders"
# #
# #     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
# #     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
# #     kiosk_id: Mapped[int] = mapped_column(ForeignKey("kiosks.id"))
# #     status: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
# #
# #     user: Mapped[List["User"]] = Relationship(back_populates="orders")
# #     kiosks: Mapped[List["Kiosks"]] = Relationship(back_populates="orders")
# #     order_stock: Mapped[List["OrderStock"]] = Relationship(back_populates="orders")
# #
# #
# class Products(Base):
#     __tablename__ = "products"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     units_meas: Mapped[int] = mapped_column(Integer, nullable=False)
#
#     kiosk_stock: Mapped[List["Kiosks"]] = Relationship(back_populates="products")
#     # order_stock: Mapped[List["OrderStock"]] = Relationship(back_populates="products")
#
#
# class KioskProduct(Base):
#     __tablename__ = "kiosk_products"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
#     kiosk_id: Mapped[int] = mapped_column(ForeignKey("kiosks.id"))
#     count: Mapped[int] = mapped_column(Integer, nullable=False)
#     price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
#
#     @hybrid_property
#     def in_stock(self):
#         stock = self.count > 0
#         return stock
#
#     products: Mapped[List["Products"]] = Relationship(back_populates="kiosk_stock")
#     kiosk: Mapped[List["Kiosks"]] = Relationship(back_populates="stock")
# #
# #
# # class OrderStock(Base):
# #     __tablename__ = "order_stock"
# #
# #     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
# #     order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
# #     product_id: Mapped[int] = mapped_column(ForeignKey(Products.id))
# #     count: Mapped[int] = mapped_column(Integer, nullable=False)
# #
# #     orders: Mapped[List["Orders"]] = Relationship(back_populates="order_stock")
# #     products: Mapped[List["Products"]] = Relationship(back_populates="order_stock")
#
# class OrderStatus(Enum):
#     NEW = "new"
#     PAID = "paid"
#     DELIVERY = "delivery"
#     DONE = "done"
#     CANCELLED = "cancelled"
#
#
# class CartItem(Base):
#     __tablename__ = 'cart'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(BigInteger, ForeignKey('user.telegram_id'))
#     kiosk_product_id = Column(Integer, ForeignKey('kiosk_products.id'))
#     count = Column(Integer, default=1)
#     user = relationship("User", back_populates="cart_items")
#     product = relationship("KioskProduct")
#
#
# class Order(Base):
#     __tablename__ = 'orders'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(BigInteger, ForeignKey('user.telegram_id'))
#     kiosk_id = Column(Integer, ForeignKey('kiosks.id'))
#     status = Column(SQLEnum(OrderStatus), default=OrderStatus.NEW)
#     cost = Column(Float, default=0.0)
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     user = relationship("User")
#     kiosk = relationship("Kiosk")
#     items = relationship("OrderItem")
#
#
# class OrderItem(Base):
#     __tablename__ = 'order_items'
#     id = Column(Integer, primary_key=True)
#     order_id = Column(Integer, ForeignKey('orders.id'))
#     kiosk_product_id = Column(Integer, ForeignKey('kiosk_products.id'))
#     count = Column(Integer)
#     price = Column(Float)
#
#     order = relationship("Order")
#     product = relationship("KioskProduct")
class OrderStatus(Enum):
    NEW = "new"
    PAID = "paid"
    DELIVERY = "delivery"
    DONE = "done"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    blocked = Column(Boolean, default=False)

    # УБИРАЕМ проблемные relationships пока
    # kiosks = relationship("Kiosk", back_populates="owner")
    cart_items = relationship("CartItem", back_populates="user")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Kiosk(Base):
    __tablename__ = 'kiosks'
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    # work_from = Column(DateTime, default=datetime.now)
    # work_util = Column(DateTime, default=datetime.now)

    # owner = relationship("User", back_populates="kiosks")
    kiosk_products = relationship("KioskProduct", back_populates="kiosk")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    products = relationship("Product", back_populates="category")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    units_meas = Column(String(20), default="шт")
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Categories", back_populates="products")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class KioskProduct(Base):
    __tablename__ = 'kiosk_products'
    id = Column(Integer, primary_key=True)
    kiosk_id = Column(Integer, ForeignKey('kiosks.id'))  # ✅ К kiosks.id
    product_id = Column(Integer, ForeignKey('products.id'))  # ✅ К products.id
    count = Column(Integer, default=0)
    price = Column(Float, default=0.0)

    kiosk = relationship("Kiosk", back_populates="kiosk_products")
    product = relationship("Product")  # ✅ БЕЗ back_populates пока

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CartItem(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # ✅ Integer для users.id
    kiosk_product_id = Column(Integer, ForeignKey('kiosk_products.id'))
    count = Column(Integer, default=1)

    user = relationship("User", back_populates="cart_items")
    kiosk_product = relationship("KioskProduct")  # ✅ НЕ product

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    kiosk_id = Column(Integer, ForeignKey('kiosks.id'))
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.NEW)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    kiosk_product_id = Column(Integer, ForeignKey('kiosk_products.id'))
    count = Column(Integer)
    price = Column(Float)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
