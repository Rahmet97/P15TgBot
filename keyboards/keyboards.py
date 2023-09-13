from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def contact_keyboard():
    contact = KeyboardButton(text="☎️ Share contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(keyboard=[[contact]], resize_keyboard=True, one_time_keyboard=True)

    return reply_markup


def location_keyboard():
    location_btn = KeyboardButton(text='📍 Share your location', request_location=True)
    reply_markup = ReplyKeyboardMarkup(keyboard=[[location_btn]], resize_keyboard=True, one_time_keyboard=True)

    return reply_markup


def client_choice():
    confirm_btn = InlineKeyboardButton(text='Confirm', callback_data='confirm')
    cancel_btn = InlineKeyboardButton(text='Cancel', callback_data='cancel')
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[[confirm_btn, cancel_btn]])

    return reply_markup
