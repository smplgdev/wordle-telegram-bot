import math

from alphabet import vowels, consonants, get_alphabet, rare_chars
from data.guess_dataclass import GuessPattern

greet_message = """<b>Привет! Сыграем в Wordle?</b> 😉

Правила игры очень простые: нужно угадать слово, состоящее из пяти букв, за 6 попыток. \
После каждой попытки цвет букв будет меняться, чтобы показать, \
какие буквы есть в загаданном слове.

🟩 <b>Зеленый цвет</b> буквы означает, что буква есть в загаданном слове и стоит на правильном месте
🟨 <b>Желтый цвет</b> буквы говорит о том, что она есть в загаданном слове, но стоит на другом месте
⬛️ Если рядом с буквой находится <b>чёрный квадрат</b>, это значит, что этой буквы в загаданном слове нет

<i>Если тебе понадобится вызвать сообщение-подсказку ещё раз, отправь команду</i> /help

Создатель бота: @smplgdev"""

game_message = "Игра началась!\n\n" + \
               "Напишите слово из пяти букв, используя свою клавиатуру"

warning_text = "Слово должно состоять из пяти русских букв. Попробуйте снова"
win_text = "Вы выиграли! Понравилась игра?"
lose_text = "Вы проиграли :(\n\nПопробуйте снова!"
game_already_started_text = "У вас уже есть начатая игра. Чтобы закончить ее, введите /start"


def get_remaining_letters_text(guess_pattern: GuessPattern):
    match = guess_pattern.get_match_chars()
    mismatch = guess_pattern.get_mismatch_chars()
    remain = guess_pattern.get_remaining_chars()
    left = remain - match - mismatch

    string = "Есть в слове: "
    if match:
        string += ' '.join(f'<b><u>{char}</u></b>' for char in list(match)[::-1]) + (' ' if mismatch else '')
    if mismatch:
        string += ' '.join(f'<b><u><i>{char}</i></u></b>' for char in mismatch if char not in match)
    if left:
        string += "\n\nОставшиеся буквы\n"
        string += ' '.join(f'{char}' for char in vowels if (char in left))
        string += '\n' + ' '.join(f'{char}' for char in consonants if (char in left))
        string += '\n' + ' '.join(f'{char}' for char in rare_chars if (char in left))

    return string


numbers_squares_dict = {
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣',
    7: '7️⃣',
    8: '8️⃣',
    9: '9️⃣',
}


def get_statistics_text(user_stats: list[int], cur_streak: int, best_streak: int) -> str | bool:

    def fill_line(attempt_: int, attempt_stats: int, all_stats: int):
        coefficient = attempt_stats / all_stats
        grn_squares = math.ceil(coefficient * 5)
        line = f'\n{numbers_squares_dict[attempt_]} ' + '🟩' * grn_squares + '⬛️' * (5 - grn_squares) + \
               f' {round(100 * wins_amount/total_games_won)}%, {attempt_stats} п.'
        return line

    total_games_won = sum(user_stats[1:])

    if total_games_won == 0:
        return "У вас слишком мало игр для статистики! " \
               "Выиграйте одну игру, чтобы получить доступ к статистике ;-)"

    string = f"<b>Ваша статистика</b>\n\n🏆 Всего побед: {total_games_won} " \
             f"({round(100 * total_games_won / user_stats[0])}%)" \
             "\n\nРаспределение побед (с какой попытки было угадано слово)"
    for attempt, wins_amount in enumerate(user_stats):
        if attempt in range(1, 6+1):
            string += fill_line(attempt, wins_amount, total_games_won)

    string += f'\n\nПобед подряд: {cur_streak}'
    string += f'\nПобед подряд максимум: {best_streak}'
    return string
