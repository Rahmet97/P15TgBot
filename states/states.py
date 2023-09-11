from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    phone = State()
    first_name = State()
    last_name = State()
    address = State()
