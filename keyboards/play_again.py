from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callback_factories import GameCallback


def get_play_again_kb(conceived_word: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Сыграть снова!", callback_data=GameCallback(action="play_again"))
    if conceived_word is not None:
        builder.button(text="Узнать загаданное слово", callback_data=GameCallback(action="show_conceived_word_if_lost",
                                                                                  conceived_word=conceived_word))
    return builder.as_markup()
