from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = "..."
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb.add(button1)
kb.add(button2)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")],  # Добавлена кнопка "Регистрация"
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ]
    ], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Рады Вас видеть!", reply_markup=start_menu)


# Блок регистрации покупателей
# --------------------
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()  


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    # await message.answer("Введите имя пользователя (только латинский алфавит):") - в задании сказано об этой строке...
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    user_name = data['username']
    add_user(data['username'], data['email'], data['age'])
    await message.answer(f"Пользователь {user_name} успешно зарегистрирован")
    await state.finish()

# --------------------

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer("Домашнее задание по теме 'Написание примитивной ORM'.")


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('"Мужчины: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A" \n'
                              '"Женщины: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A"')
    await call.answer()


class UserState(StatesGroup):
    gender = State()
    weight = State()
    height = State()
    age = State()
    active = State()


@dp.callback_query_handler(text='calories')
async def gender(call):
    await call.message.answer("Укажите Ваш пол: мужской - 'м', женский - 'ж'")
    await call.answer()
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def fsm_gender(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Укажите Ваш вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def fsm_weight(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Укажите Ваш рост')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def fsm_height(message, state):
    await state.update_data(height=message.text)
    await message.answer('Укажите Ваш возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def fsm_age(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите коэффициент Вашей активности: \n'
                         'Минимальная активность: A = 1.2. \n'
                         'Слабая активность: A = 1.375. \n'
                         'Средняя активность: A = 1.55. \n'
                         'Высокая активность: A = 1.725. \n'
                         'Экстра-активность: A = 1.9')
    await UserState.active.set()


@dp.message_handler(state=UserState.active)
async def fsm_result(message, state):
    await state.update_data(active=message.text)
    data = await state.get_data()
    w = int(data['weight'])
    h = int(data['height'])
    a = int(data['age'])
    act = float(data['active'])
    if data['gender'] == 'м':
        await message.answer(f"Ваша суточная норма {((10 * w) + (6.25 * h) - (5 * a) + 5) * act} калорий.")
    else:
        await message.answer(f"Ваша суточная норма {((10 * w) + (6.25 * h) - (5 * a) - 161) * act} калорий.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)