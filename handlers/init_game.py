import json

from aiogram import Router, F
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot import bot
from data.guess_dataclass import GuessPattern
from data.word_dataclass import Word
from keyboards.callback_factories import GameCallback
from keyboards.game_kb import make_kb_from_guesses
from keyboards.play_again import get_play_again_kb
from src import strings
from states.guess_word import GuessWord

router = Router()


@router.callback_query(GameCallback.filter(F.action == "play_again"))
@router.callback_query(GameCallback.filter(F.action == "start"))
async def init_game(call: types.CallbackQuery, state: FSMContext):
    """
        Sends messages with game template
    """

    # Removes buttons from greet message or play again message
    await call.message.delete_reply_markup()

    conceived_word = Word().conceive()
    await state.set_state(GuessWord.guessing_word)

    game_message = strings.game_message
    message = await call.message.answer(game_message, reply_markup=make_kb_from_guesses())

    gp = GuessPattern()
    string = strings.get_remaining_letters_text(gp)
    await call.message.answer(string)

    with open(f"data/userdata/{call.from_user.id}-{message.message_id}.txt", "w", encoding="utf8") as f:
        f.write(conceived_word)

    await state.update_data(game_msg_id=message.message_id)


@router.message(GuessWord.guessing_word)
async def guess_word(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_word = message.text.lower().replace('ё', 'е')

    if not Word.is_user_input_correct(user_word):
        await message.delete()
        await message.answer(strings.warning_text)
        return
    game_msg_id = int(data.get("game_msg_id"))

    with open(f"data/userdata/{message.from_user.id}-{game_msg_id}.txt", 'r', encoding='utf8') as f:
        conceived_word = f.readline().strip()

    guess_pattern = Word(conceived_word).get_guess_pattern(user_word)
    guess_to_json = [{"char": char.char, "status": char.status} for char in guess_pattern]

    with open(f"data/userdata/{message.from_user.id}-{game_msg_id}.txt", 'a', encoding='utf8') as f:
        json_str = json.dumps(guess_to_json)
        f.write('\n' + json_str)

    with open(f"data/userdata/{message.from_user.id}-{game_msg_id}.txt", 'r', encoding='utf8') as f:
        guesses = f.readlines()[1:]

    guesses = [json.loads(guess.strip()) for guess in guesses]

    gp = GuessPattern(guesses)

    markup = make_kb_from_guesses(gp)
    await bot.edit_message_reply_markup(message.from_user.id, game_msg_id, reply_markup=markup)

    if all(char.status == "match" for char in guess_pattern):
        await message.answer(strings.win_text,
                             reply_markup=get_play_again_kb())
        await state.clear()
        return

    # editing remaining letters message:
    remain_letters = strings.get_remaining_letters_text(gp)
    try:
        await bot.edit_message_text(remain_letters, message.from_user.id, game_msg_id+1)
    except TelegramBadRequest:
        pass

    tries = len(guesses)

    if tries == 6:
        await message.answer(strings.lose_text,
                             reply_markup=get_play_again_kb(conceived_word=conceived_word))
        await state.clear()
        return

    await state.update_data(tries=tries)
    await message.delete()
