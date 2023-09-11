import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

from code import get_address_using_location
from databases.database import create_user_table, insert_data
from states.states import UserState

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def startup(message: Message, state: FSMContext):
    first_name = message.from_user.first_name
    contact = KeyboardButton(text="☎️ Share contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(keyboard=[[contact]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(
        f"Hello {first_name}! Please share your contact.",
        reply_markup=reply_markup
    )
    await message.delete()
    await state.set_state(UserState.phone)


@dp.message(UserState.phone)
async def phone(message: Message, state: FSMContext):
    contact = message.contact
    await state.update_data({
        'phone': contact.phone_number
    })
    await message.answer('Enter your first name')
    await state.set_state(UserState.first_name)


@dp.message(UserState.first_name)
async def first_name(message: Message, state: FSMContext):
    await state.update_data({
        'first_name': message.text
    })
    await message.answer('Enter your last name')
    await state.set_state(UserState.last_name)


@dp.message(UserState.last_name)
async def last_name(message: Message, state: FSMContext):
    await state.update_data({
        'last_name': message.text
    })
    location_btn = KeyboardButton(text='📍 Share your location', request_location=True)
    reply_markup = ReplyKeyboardMarkup(keyboard=[[location_btn]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Share your location', reply_markup=reply_markup)
    await state.set_state(UserState.address)


@dp.message(UserState.address)
async def address(message: Message, state: FSMContext):
    location = message.location
    lon = location.longitude
    lat = location.latitude
    city = get_address_using_location(lat, lon)
    await state.update_data({
        'address': city
    })
    data = await state.get_data()
    phone = data['phone']
    first_name = data['first_name']
    last_name = data['last_name']
    address = data['address']
    msg = f'''
📞 Phone number: {phone}
🧍‍♂️First name: {first_name}
🧍‍♂️Last name: {last_name}
🌍Address: {address}
    '''
    confirm_btn = InlineKeyboardButton(text='Confirm', callback_data='confirm')
    cancel_btn = InlineKeyboardButton(text='Cancel', callback_data='cancel')
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[confirm_btn, cancel_btn]])
    await message.answer(msg, reply_markup=reply_markup)


@dp.callback_query(lambda callback_query: callback_query.data == 'confirm')
async def confirm(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_data = dict(
        phone=data['phone'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        address=data['address']
    )
    insert_data(user_data)
    await state.storage.close()
    await state.clear()
    await callback_query.message.answer('Successfully registered!')
    await callback_query.message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'cancel')
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    await state.storage.close()
    await state.clear()
    await callback_query.message.answer('Canceled. Please try again')
    await callback_query.message.delete()
    first_name = callback_query.message.from_user.first_name
    contact = KeyboardButton(text="☎️ Share contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(keyboard=[[contact]], resize_keyboard=True, one_time_keyboard=True)
    await callback_query.message.answer(
        f"Hello {first_name}! Please share your contact.",
        reply_markup=reply_markup
    )
    await state.set_state(UserState.phone)


@dp.message(lambda msg: msg.text == '/help')
async def help_function(message: Message):
    await message.answer('Welcome to our bot!')


async def main():
    bot = Bot(TOKEN)
    create_user_table()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
