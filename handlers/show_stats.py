from aiogram import Router, F, types
from aiogram.filters import Command

from database.pgcommands import user as user_commands
from keyboards.callback_factories import GameCallback
from src import strings

router = Router()


@router.callback_query(GameCallback.filter(F.action == "show_stats"))
async def show_user_stats(call: types.CallbackQuery):
    await call.answer(cache_time=10)
    user_stats_dict = await user_commands.get_user_statistics(call.from_user.id)
    user_stats = user_stats_dict['user_stats']
    cur_streak = user_stats_dict['cur_streak']
    best_streak = user_stats_dict['best_streak']
    stats_text = strings.get_statistics_text(user_stats, cur_streak, best_streak)
    await call.message.answer(stats_text)


@router.message(Command('stats'))
async def show_stats_command_handler(message: types.Message):
    user_stats_dict = await user_commands.get_user_statistics(message.from_user.id)
    user_stats = user_stats_dict['user_stats']
    cur_streak = user_stats_dict['cur_streak']
    best_streak = user_stats_dict['best_streak']
    stats_text = strings.get_statistics_text(user_stats, cur_streak, best_streak)
    await message.answer(stats_text)
