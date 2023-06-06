from aiogram.types import Message, InputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from main import dp
import text
import sql
from states import Category


@dp.message_handler(Command('start'))
async def start_handler(message: Message, state=None):
    """ Приветствие пользователя """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/help")
    markup.add(btn)
    await message.answer(text.hello, reply_markup=markup)


@dp.message_handler(Command('help'))
async def help(message: Message):
    await message.answer(text.help)


@dp.message_handler(Command('find'))
async def find(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_type, reply_markup=markup)
    await Category.type.set()


@dp.message_handler(state=Category.type)
async def ask_type(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(type=message.text)
    else:
        await state.update_data(type="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_min_price, reply_markup=markup)
    await Category.next()


@dp.message_handler(state=Category.min_price)
async def ask_min_price(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(min_price=int(message.text))
    else:
        await state.update_data(min_price="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_max_price, reply_markup=markup)
    await Category.next()


@dp.message_handler(state=Category.max_price)
async def ask_max_price(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(max_price=int(message.text))
    else:
        await state.update_data(max_price="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_country, reply_markup=markup)
    await Category.next()


@dp.message_handler(state=Category.country)
async def ask_country(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(country=message.text)
    else:
        await state.update_data(country="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_year, reply_markup=markup)
    await Category.next()


@dp.message_handler(state=Category.year)
async def ask_year(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(year=int(message.text))
    else:
        await state.update_data(year="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_marka, reply_markup=markup)
    await Category.next()


@dp.message_handler(state=Category.marka)
async def ask_marka(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(marka=message.text)
    else:
        await state.update_data(marka="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/next")
    markup.add(btn)
    await message.answer(text.ask_model, reply_markup=markup)
    await Category.next()


@dp.message_handler(state=Category.model)
async def ask_model(message: Message, state: FSMContext):
    if message.text != "/next":
        await state.update_data(model=message.text)
    else:
        await state.update_data(model="")
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/find")
    markup.add(btn)
    await message.answer(text.show)
    await Category.next()
    await show(message, state)


@dp.message_handler(state=Category.show)
async def show(message: Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/find")
    markup.add(btn)
    get_c = await state.get_data()
    category = [get_c['country'], get_c['type'], get_c['min_price'],
                get_c['max_price'], get_c['year'], get_c['marka'], get_c['model'], ]
    info = await sql.find(category)
    if len(info) == 0:
        await message.answer(text.now_car)
    for data in info:
        photo = InputFile("pictures/" + str(data[0]) + ".jpg")
        caption = f"Марка: {data[1]} \n" \
                  f"Модель: {data[2]} \n" \
                  f"Класс: {data[3]} \n" \
                  f"Год выпуска: {data[4]} \n" \
                  f"Цена: {data[5]} \n" \
                  f"Страна производителя: {data[6]}"
        await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)
    await state.finish()
