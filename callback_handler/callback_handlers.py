from dispatcher import dp
from databases.database import insert_data
from keyboards.keyboards import contact_keyboard
from states.states import UserState

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


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
    reply_markup = contact_keyboard()
    await callback_query.message.answer(
        f"Hello {first_name}! Please share your contact.",
        reply_markup=reply_markup
    )
    await state.set_state(UserState.phone)
