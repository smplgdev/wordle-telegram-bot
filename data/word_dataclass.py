import re

from data.char_dataclass import Char


class Word:
    def __init__(self, word: str = None):
        self.word = word
        self.index: int | None = None

    def conceive(self):
        from random import randint

        with open("toconceivewords.txt", "r", encoding='utf8') as f:
            words_array = f.readlines()
            random_index = randint(0, len(words_array) - 1)
            word = words_array[random_index].strip().lower()

        self.word = word
        self.index = random_index
        return self.word

    @staticmethod
    def has_cyrillic(text):
        return bool(re.search('[а-яА-Я]', text))

    @staticmethod
    def is_user_input_correct(word: str) -> bool:
        if len(word) != 5:
            return False
        if not Word.has_cyrillic(word):
            return False
        with open('extended_wordlist.txt', 'r', encoding='utf8') as f:
            array = tuple(map(lambda line: line.strip(), f.readlines()))
            if word not in array:
                return False
        return True

    def get_guess_pattern(self, user_input_word: str):
        guess_pattern = list()

        conceived_word = self.word
        for i, char in enumerate(user_input_word):
            if user_input_word[i] == conceived_word[i]:
                guess_pattern.append(Char(char, 'match'))
            elif char in conceived_word and conceived_word.count(char) == user_input_word.count(char):
                guess_pattern.append(Char(char, 'mismatch'))
            else:
                guess_pattern.append(Char(char, 'missing'))
        return guess_pattern
