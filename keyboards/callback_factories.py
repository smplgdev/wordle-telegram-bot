from typing import Optional

from aiogram.filters.callback_data import CallbackData


class GameCallback(CallbackData, prefix="game"):
    action: str
    conceived_word: Optional[str]
