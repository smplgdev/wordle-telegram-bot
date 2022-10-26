from aiogram import Router, F, types

from keyboards.start_kb import get_start_kb
from src import strings

router = Router()


@router.message()
async def no_state_handler(message: types.Message):
    markup = get_start_kb()
    greet_message = strings.greet_message
    await message.answer(greet_message, reply_markup=markup)
