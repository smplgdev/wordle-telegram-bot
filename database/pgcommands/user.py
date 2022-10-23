from asyncpg import UniqueViolationError

from database.models.User import User


async def add_user(tg_id: int, deep_link: str = None, username: str = None):
    user = User(tg_id=tg_id, deep_link=deep_link, username=username)
    try:
        await user.create()
    except UniqueViolationError:
        pass
    return user
