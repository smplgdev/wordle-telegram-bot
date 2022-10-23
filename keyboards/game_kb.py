import json

from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data.char_dataclass import Char
from data.guess_dataclass import GuessPattern

squares = {
    'match': '🟩',
    'mismatch': '🟨',
    'missing': '⬛️',
}


def create_empty_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[]])


def add_empty_kb_row(markup: InlineKeyboardMarkup | None = None) -> InlineKeyboardMarkup:
    if not markup:
        markup = create_empty_markup()

    kb = markup.inline_keyboard
    kb.append([
        InlineKeyboardButton(text="—", callback_data="null")] * 5
    )
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def add_empty_row(builder: InlineKeyboardBuilder):
    builder.row(*[
            InlineKeyboardButton(text="—", callback_data="null")
        ] * 5
    )
    return builder


def add_guess_to_kb(markup: InlineKeyboardMarkup, guess_pattern: list[Char]) -> object:
    kb = markup.inline_keyboard
    layer = [InlineKeyboardButton(text=f"{squares[char.status]} {char.char}",
                                  callback_data='null') for char in guess_pattern]
    kb[-1] = layer
    for _ in range(6-len(kb)):
        kb = add_empty_kb_row(kb)
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def make_kb_from_guesses(guesses: GuessPattern | None = None):
    builder = InlineKeyboardBuilder()
    count = 0

    if guesses:
        for guess_pattern in guesses.list_patterns():
            row = []
            for char in guess_pattern:
                row.append(InlineKeyboardButton(text=f"{squares[char.status]} {char.char.upper()}",
                                                callback_data="null"))
            builder.row(*row)
            count += 1

    for _ in range(6-count):
        add_empty_row(builder)

    return builder.as_markup()
