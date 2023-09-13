from aiogram.types.bot_command import BotCommand
from aiogram.filters.command import Command
from aiogram.types import Message

from dispatcher import dp
from keyboards.keyboards import location_keyboard

start = BotCommand(command='start', description='Start bot')
help = BotCommand(command='help', description='Help command')
weather = BotCommand(command='weather', description='Weather in your current location')


@dp.message(Command(help))
async def help_function(message: Message):
    await message.answer('Welcome to our bot!')


@dp.message(Command(weather))
async def weather_command(message: Message):
    reply_markup = location_keyboard()
    await message.answer("Share your location", reply_markup=reply_markup)
