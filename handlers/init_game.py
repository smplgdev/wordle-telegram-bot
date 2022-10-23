from aiogram import Router, F
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot import bot
from database.pgcommands import game as game_commands
from database.pgcommands import guesses as guess_commands
from data.guess_dataclass import GuessPattern
from data.word_dataclass import Word
from keyboards.callback_factories import GameCallback
from keyboards.game_kb import make_kb_from_guesses
from keyboards.play_again import get_play_again_kb
from src import strings
from states.guess_word import GuessWord

router = Router()


@router.callback_query(GameCallback.filter(F.action.in_(["play_again",
                                                         "start"])),
                       F.state == GuessWord.guessing_word)
async def cancel_game_init(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("У вас уже есть начатая игра. Чтобы закончить ее, введите /start")
    await state.clear()
    await init_game(call, state)


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

    message = await call.message.answer(strings.game_message, reply_markup=make_kb_from_guesses())

    game = await game_commands.initialize_game(game_message_id=message.message_id,
                                               user_telegram_id=call.from_user.id,
                                               conceived_word=conceived_word)
    gp = GuessPattern()
    string = strings.get_remaining_letters_text(gp)
    await call.message.answer(string)
    await state.update_data(game_id=game.id)


@router.message(GuessWord.guessing_word)
async def guess_word(message: types.Message, state: FSMContext):
    user_word = message.text.lower().replace('ё', 'е')

    if not Word.is_user_input_correct(user_word):
        await message.delete()
        await message.answer(strings.warning_text)
        return

    data = await state.get_data()
    game_id = int(data.get("game_id"))

    game = await game_commands.get_game_by_id(game_id)
    game_msg_id = game.game_message_id

    await guess_commands.add_guess(game_id=game_id,
                                   word=user_word)

    guesses = await guess_commands.get_game_guesses_words(game_id)
    # guesses.append(user_word)

    guesses_patterns = list()
    for guess in guesses:
        guesses_patterns.append(Word(game.conceived_word).get_guess_pattern(guess[0]))

    gp = GuessPattern(guesses_patterns)
    markup = make_kb_from_guesses(gp)
    await bot.edit_message_reply_markup(message.from_user.id, game_msg_id, reply_markup=markup)

    if all(char.status == "match" for char in guesses_patterns[-1]):
        await message.answer(strings.win_text,
                             reply_markup=get_play_again_kb())
        await game_commands.update_game_status(game_id, "end")
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
                             reply_markup=get_play_again_kb(conceived_word=game.conceived_word))
        await state.clear()
        return

    await message.delete()
