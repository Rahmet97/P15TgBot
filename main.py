import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from dotenv import load_dotenv

from code import get_temperature

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()
DATA = None


@dp.message(CommandStart())
async def startup(message: Message):
    first_name = message.from_user.first_name
    await message.answer(f"Hello {first_name}!")


@dp.message(lambda msg: msg.text == '/weather')
async def weather(message: Message):
    await message.answer("Please enter your city name")


@dp.message(lambda msg: msg.text in ['Maximum temperature', 'Minimum temperature', 'Pressure', 'Humidity'])
async def click(message: Message):
    dtb = None
    match message.text:
        case 'Maximum temperature':
            dtb = DATA['main']['temp_max']
        case 'Minimum temperature':
            dtb = DATA['main']['temp_min']
        case 'Pressure':
            dtb = DATA['main']['pressure']
        case 'Humidity':
            dtb = DATA['main']['humidity']

    await message.answer(str(dtb))


@dp.message()
async def show_weather(message: Message):
    city = message.text
    response = get_temperature(city)
    if response['cod'] != "404":
        text = f'Temperature: {response["main"]["temp"]}'
        global DATA
        DATA = response
        max_temp_btn = KeyboardButton(text='Maximum temperature')
        min_temp_btn = KeyboardButton(text='Minimum temperature')
        pressure_btn = KeyboardButton(text='Pressure')
        humidity_btn = KeyboardButton(text='Humidity')
        reply_markup = ReplyKeyboardMarkup(keyboard=[[max_temp_btn], [min_temp_btn], [pressure_btn], [humidity_btn]], resize_keyboard=True)
        await message.answer(text, reply_markup=reply_markup)
    else:
        text = 'City not found, please try again!'
        await message.answer(text)


@dp.message(lambda msg: msg.text == '/help')
async def help_function(message: Message):
    await message.answer('Welcome to our bot!')


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
