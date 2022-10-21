from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == 'null')
async def call_answer_none(call: CallbackQuery):
    """
    Activates when user taps game board
    """
    await call.answer(cache_time=60)
