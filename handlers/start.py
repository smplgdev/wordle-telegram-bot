from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.pgcommands import user as user_commands
from keyboards.start_kb import get_start_kb
from src import strings

router = Router()


@router.message(Command('help'))
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    deep_link = get_deep_link(message.text)
    await user_commands.add_user(tg_id=message.from_user.id,
                                 deep_link=deep_link,
                                 username=message.from_user.username)

    markup = get_start_kb()
    greet_message = strings.greet_message
    await message.answer(greet_message, reply_markup=markup)


def get_deep_link(message_text: str):
    m = message_text.split()
    if len(m) > 1:
        return m[1]
    return None
