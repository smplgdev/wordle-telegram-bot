from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.callback_factories import GameCallback

router = Router()


@router.callback_query(GameCallback.filter(F.action == 'show_conceived_word_if_lost'))
async def show_conceived_word_if_lost_handler(call: CallbackQuery, callback_data: GameCallback):
    await call.answer("Было загадано слово: " + callback_data.conceived_word.upper(),
                      show_alert=True)
