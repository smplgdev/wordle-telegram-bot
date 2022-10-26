import logging
import asyncio
from aiogram import Bot, Dispatcher

from database.db_gino import db
from handlers import init_game, start, query_handler_none, show_conceived_word_if_lost, no_state_handler, show_stats
from config import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode='HTML')
ADMINS = config.ADMINS

POSTGRES_URI = f'postgresql://{config.PG_USERNAME}:{config.PG_PASSWORD}@{config.ip}/{config.PG_DATABASE}'


async def main():
    logging.info("Setup connection with PostgreSQL")
    await db.set_bind(POSTGRES_URI)

    # logging.info("Drop models")
    # await db.gino.drop_all()

    logging.info("Create models")
    await db.gino.create_all()

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(show_stats.router)
    dp.include_router(show_conceived_word_if_lost.router)
    dp.include_router(query_handler_none.router)
    dp.include_router(init_game.router)
    dp.include_router(no_state_handler.router)

    # Launch bot & skip all missed messages
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
