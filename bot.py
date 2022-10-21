import logging
import asyncio
from aiogram import Bot, Dispatcher

from handlers import init_game, start, query_handler_none, show_conceived_word_if_lost
from config import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode='HTML')


async def main():
    logging.info("Starting bot...")

    dp = Dispatcher()

    dp.include_router(show_conceived_word_if_lost.router)
    dp.include_router(query_handler_none.router)
    dp.include_router(init_game.router)
    dp.include_router(start.router)

    # Launch bot & skip all missed messages
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
