from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callback_factories import GameCallback


def get_start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # ./handlers/init_game.py/init_game()
    builder.button(text="Начать игру", callback_data=GameCallback(action='start'))

    return builder.as_markup()
