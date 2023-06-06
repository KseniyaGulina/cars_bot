from aiogram.dispatcher.filters.state import State, StatesGroup


class Category(StatesGroup):
    type = State()
    min_price = State()
    max_price = State()
    country = State()
    year = State()
    marka = State()
    model = State()
    show = State()
    stop = State()
