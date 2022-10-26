from asyncpg import UniqueViolationError
from sqlalchemy import and_

from database.models.Game import Game
from database.models.User import User
from database.pgcommands import guesses as guess_commands, conceive_words


async def add_user(tg_id: int, deep_link: str = None, username: str = None):
    user = User(tg_id=tg_id, deep_link=deep_link, username=username)
    try:
        await user.create()
    except UniqueViolationError:
        pass
    return user


async def get_user_statistics(user_tg_id: int) -> dict:
    user_stats = list([0] * 7)
    games = await Game.query.where(and_(Game.user_telegram_id == user_tg_id,
                                        Game.status not in ['ext', 'end'])).gino.all()
    user_stats[0] = len(games)
    best_streak = 0
    cur_streak = 0
    for game in games:
        if game.status == 'win':
            cur_streak += 1
            best_streak = max(cur_streak, best_streak)
        else:
            cur_streak = 0
        guesses = await guess_commands.get_game_guesses_words(game.id)
        if len(guesses) < 1:
            continue
        guesses = [guess.user_input_word for guess in guesses]

        conceive_word = await conceive_words.get_by_id(game.conceived_word_id)

        if conceive_word == guesses[-1] and game.status == 'win':
            user_stats[len(guesses)] += 1
    return {'user_stats': user_stats, 'cur_streak': cur_streak, 'best_streak': best_streak}
