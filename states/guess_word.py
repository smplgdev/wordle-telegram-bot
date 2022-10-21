from aiogram.fsm.state import State, StatesGroup


class GuessWord(StatesGroup):
    guessing_word = State()
