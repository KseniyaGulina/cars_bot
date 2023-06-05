from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Category(StatesGroup):
    country = State()
    type = State()
    min_price = State()
    max_price = State()
    year = State()
    marka = State()
    model = State()
    stop = State()