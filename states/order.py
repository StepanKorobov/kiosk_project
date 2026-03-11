from telebot.handler_backends import State, StatesGroup


class Order(StatesGroup):
    choice = State()
