from typing import List

from sqlalchemy import create_engine, Integer, String, Boolean, func, Float, DECIMAL, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase, Relationship
from sqlalchemy.ext.hybrid import hybrid_property

engine = create_engine("sqlite:///database.db")
session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    telegram_id: Mapped[int] = mapped_column(String, nullable=False, unique=True)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    kiosk_owner: Mapped[List["Kiosks"]] = Relationship(back_populates="owner")
    orders: Mapped[List["Orders"]] = Relationship(back_populates="user")


class Kiosks(Base):
    __tablename__ = "kiosks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    owner: Mapped[List["User"]] = Relationship(back_populates="kiosk_owner")
    orders: Mapped[List["Orders"]] = Relationship(back_populates="kiosks")
    stock: Mapped[List["KioskStock"]] = Relationship(back_populates="kiosk")


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    kiosk_id: Mapped[int] = mapped_column(ForeignKey("kiosks.id"))
    status: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    user: Mapped[List["User"]] = Relationship(back_populates="orders")
    kiosks: Mapped[List["Kiosks"]] = Relationship(back_populates="orders")
    order_stock: Mapped[List["OrderStock"]] = Relationship(back_populates="orders")


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    units_meas: Mapped[int] = mapped_column(Integer, nullable=False)

    kiosk_stock: Mapped[List["Kiosks"]] = Relationship(back_populates="products")
    order_stock: Mapped[List["OrderStock"]] = Relationship(back_populates="products")


class KioskStock(Base):
    __tablename__ = "kiosk_stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    kiosk_id: Mapped[int] = mapped_column(ForeignKey("kiosks.id"))
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)

    @hybrid_property
    def in_stock(self):
        stock = self.count > 0
        return stock

    products: Mapped[List["Products"]] = Relationship(back_populates="kiosk_stock")
    kiosk: Mapped[List["Kiosks"]] = Relationship(back_populates="stock")


class OrderStock(Base):
    __tablename__ = "order_stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey(Products.id))
    count: Mapped[int] = mapped_column(Integer, nullable=False)

    orders: Mapped[List["Orders"]] = Relationship(back_populates="order_stock")
    products: Mapped[List["Products"]] = Relationship(back_populates="order_stock")
