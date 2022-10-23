from database.models.Guess import Guess


async def add_guess(game_id: int, word: str):
    guess = Guess(game_id=game_id,
                  user_input_word=word)
    await guess.create()
    return guess


async def get_game_guesses_words(game_id: int) -> list[str]:
    guesses = await Guess.select('user_input_word').where(Guess.game_id == game_id).gino.all()
    return guesses
