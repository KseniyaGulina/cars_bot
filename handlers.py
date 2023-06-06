from aiogram.types import Message, InputFile, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp
import text
import sql
import vars
from states import Category


@dp.message_handler(Command('start'))
async def start_handler(message: Message, state=None):
    """ Приветствие пользователя """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("/help")
    markup.add(btn)
    await message.answer(text.hello, reply_markup=markup)


@dp.message_handler(Command('help'))
async def help(message: Message, state=None):
    await message.answer(text.help)


@dp.message_handler(Command('stop'))
async def find(message: Message, state=FSMContext):
    await message.answer(text.stop)
    await state.finish()


@dp.message_handler(Command('find'))
async def find(message: Message, state=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_type, reply_markup=markup)
    await Category.type.set()
    vars.state_now += 1


@dp.message_handler(state=Category.type)
async def ask_type(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.type = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_min_price, reply_markup=markup)
    await Category.next()
    # vars.state_now += 1


@dp.message_handler(state=Category.min_price)
async def ask_min_price(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.min_price = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_max_price, reply_markup=markup)
    await Category.next()
    # await Category.min_price.set()
    # vars.state_now += 1


@dp.message_handler(state=Category.max_price)
async def ask_max_price(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.max_price = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_country, reply_markup=markup)
    # await Category.min_price.set()
    # vars.state_now += 1
    await Category.next()


@dp.message_handler(state=Category.country)
async def ask_country(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.country = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_year, reply_markup=markup)
    # await Category.min_price.set()
    # vars.state_now += 1
    await Category.next()


@dp.message_handler(state=Category.year)
async def ask_year(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.year = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_marka, reply_markup=markup)
    # await Category.min_price.set()
    # vars.state_now += 1
    await Category.next()


@dp.message_handler(state=Category.marka)
async def ask_marka(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.marka = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.ask_model, reply_markup=markup)
    # await Category.min_price.set()
    # vars.state_now += 1
    await Category.next()


@dp.message_handler(state=Category.model)
async def ask_model(message: Message, state=FSMContext):
    async with state.proxy() as data:
        vars.model = message.text
    # ПРОВЕРИТЬ ТИП ДАННЫХ
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/stop")
    btn2 = KeyboardButton("/next")
    btn3 = KeyboardButton("/show")
    markup.add(btn1, btn2, btn3)
    await message.answer(text.show)
    # await Category.min_price.set()
    # vars.state_now += 1
    await Category.next()
    vars.data = await sql.find(vars.marka)
    await show(message)


@dp.message_handler(state=Category.show)
async def show(message: Message, state=FSMContext):
    # mark = message.text.split()[-1]
    info = await sql.find(vars.marka)
    for data in info:
        photo = InputFile("pictures/" + str(data[0]) + ".jpg")
        caption = f"Марка = {data[1]} \n" \
                  f"Год выпуска = {data[4]} \n" \
                  f"Цена = {data[3]}"
        await message.answer_photo(photo=photo, caption=caption)


@dp.message_handler(Command('stop'))
async def stop(message: Message, state=FSMContext):
    vars.state_now = 0
    vars.country = ""
    vars.type = ""
    vars.min_price = ""
    vars.max_price = ""
    vars.year = ""
    vars.marka = ""
    vars.model = ""
    await state.finish()
    # await Category.stop.set()


@dp.message_handler(state=Category.show)
async def show_a(message: Message, state=FSMContext):
    # mark = message.text.split()[-1]
    info = await sql.find(vars.marka)
    data = info[0]
    # data = info
    # del info[0]
    # photo = InputFile("pictures/" + data[2])
    photo = InputFile("pictures/" + str(data[0]) + ".jpg")
    caption = f"Марка = {data[1]} \n" \
              f"Год выпуска = {data[4]} \n" \
              f"Цена = {data[3]}"
    await message.answer_photo(photo=photo, caption=caption)

    @dp.message_handler(lambda message: message.text == "Дальше")
    async def without_puree(message: Message):
        data = info[0]
        del info[0]
        photo = InputFile("pictures/" + data[2])
        caption = f"Марка = {data[1]} \n" \
                  f"Год выпуска = {data[4]} \n" \
                  f"Цена = {data[3]}"
        await message.answer_photo(photo=photo, caption=caption)


@dp.message_handler(Command('show'))
async def show_a(message: Message, state=FSMContext):
    mark = message.text.split()[-1]
    info = await sql.find(mark)
    data = info[0]
    del info[0]
    # photo = InputFile("pictures/" + data[2])
    photo = InputFile("pictures/" + data[0] + ".jpg")
    caption = f"Марка = {data[1]} \n" \
              f"Год выпуска = {data[4]} \n" \
              f"Цена = {data[3]}"
    await message.answer_photo(photo=photo, caption=caption)

    @dp.message_handler(lambda message: message.text == "Дальше")
    async def without_puree(message: Message):
        data = info[0]
        del info[0]
        photo = InputFile("pictures/" + data[2])
        caption = f"Марка = {data[1]} \n" \
                  f"Год выпуска = {data[4]} \n" \
                  f"Цена = {data[3]}"
        await message.answer_photo(photo=photo, caption=caption)
