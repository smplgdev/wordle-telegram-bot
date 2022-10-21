from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.st import get_start_kb
from src import strings

router = Router()


@router.message(Command('help'))
@router.message(CommandStart)
async def cmd_start(message: Message):
    markup = get_start_kb()
    greet_message = strings.greet_message
    await message.answer(greet_message, reply_markup=markup)
