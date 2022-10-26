import random

from asyncpg import UniqueViolationError

from database.models.Conceive_word import ConceiveWord


async def get_random_conceive_word() -> ConceiveWord:
    word = random.choice([
        word for word in await ConceiveWord.query.gino.all()
    ])
    return word


async def get_by_id(word_id: int) -> str:
    return (await ConceiveWord.get(word_id)).word


async def get_id_by_word(word: str) -> int:
    return (await ConceiveWord.query.where(ConceiveWord.word == word).gino.first()).id


async def add_word(word: str) -> ConceiveWord:
    conceive_word = ConceiveWord(word=word)
    try:
        conceive_word.create()
    except UniqueViolationError:
        pass
    return conceive_word
