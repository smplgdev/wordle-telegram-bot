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


def get_remaining_letters_text(guess_pattern: GuessPattern):
    match = guess_pattern.get_match_chars()
    mismatch = guess_pattern.get_mismatch_chars()
    remain = guess_pattern.get_remaining_chars()
    left = remain - match - mismatch

    string = "Оставшиеся буквы\n"
    if match:
        string += '\n' + ' '.join(f'<b><u>{char}</u></b>' for char in list(match)[::-1]) + (' ' if mismatch else '')
    if mismatch:
        if not match:
            string += '\n'
        string += ' '.join(f'<b><u><i>{char}</i></u></b>' for char in mismatch if char not in match)
    if left:
        string += '\n' + ' '.join(f'{char}' for char in vowels if (char in left))
        string += '\n' + ' '.join(f'{char}' for char in consonants if (char in left))
        string += '\n' + ' '.join(f'{char}' for char in rare_chars if (char in left))

    return string
