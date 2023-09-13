import os
import asyncio

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

from code import get_address_using_location, get_temperature
from databases.database import create_user_table
from keyboards.keyboards import contact_keyboard, location_keyboard, client_choice
from states.states import UserState
from dispatcher import dp
from commands.commands import start, help, weather
from callback_handler import callback_handlers

load_dotenv()


@dp.message(CommandStart())
async def startup(message: Message, state: FSMContext):
    first_name = message.from_user.first_name
    reply_markup = contact_keyboard()
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
    await message.answer('Enter your first name', reply_markup=ReplyKeyboardRemove())
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
    reply_markup = location_keyboard()
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
    await message.answer('Confirm or Cancel', reply_markup=ReplyKeyboardRemove())
    reply_markup = client_choice()
    await message.answer(msg, reply_markup=reply_markup)


@dp.message(lambda msg: msg.location is not None)
async def get_weather(message: Message):
    location = message.location
    lon = location.longitude
    lat = location.latitude
    temp = get_temperature(lat, lon)
    await message.answer(str(round(temp['main']['temp'], 1)) + '°C', reply_markup=ReplyKeyboardRemove())


async def main():
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token)
    create_user_table()
    await bot.set_my_commands(commands=[start, help, weather])
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
