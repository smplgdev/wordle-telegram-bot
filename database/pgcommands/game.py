import datetime
from datetime import timezone

from database.models.Game import Game


async def get_game_by_id(game_id: int) -> Game:
    game = await Game.query.where(Game.id == game_id).gino.first()
    return game


async def initialize_game(game_message_id: int, user_telegram_id: int, conceived_word_id: str) -> Game:
    game = Game(game_message_id=game_message_id,
                user_telegram_id=user_telegram_id,
                conceived_word_id=conceived_word_id,
                date=datetime.datetime.now(timezone.utc),
                status='run')
    await game.create()
    return game


async def update_game_status(game_id: int, status: str):
    game = await Game.get(game_id)
    await game.update(status=status).apply()


async def get_all_games() -> list[Game]:
    return await Game.query.gino.all()


async def update_word_id(game: Game, word_id: int):
    await game.update(conceived_word_id=word_id).apply()
