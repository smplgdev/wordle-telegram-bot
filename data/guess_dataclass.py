import json

from alphabet import get_alphabet
from data.char_dataclass import Char


class GuessPattern:
    def __init__(self, guesses: list[list] = None):
        self.chars = set()
        if guesses is not None:
            self.chars = [
                Char(
                    char=char['char'] if type(char) == dict else char.__dict__['char'],
                    status=char['status'] if type(char) == dict else char.__dict__['status']
                ) for guess in guesses for char in guess if guesses
            ]
        self.guesses = guesses if guesses else [[]]

    def get_match_chars(self) -> set:
        array = set([char.char.upper() for char in self.chars if char.status == 'match'])
        return array

    def get_mismatch_chars(self) -> set:
        array = set([char.char.upper() for char in self.chars if char.status == 'mismatch'])
        return array

    def get_missing_chars(self) -> set:
        array = set([char.char.upper() for char in self.chars if char.status == 'missing'])
        return array

    def get_used_chars(self) -> set:
        used_letters = set([char.char.upper() for char in self.chars if char.status == 'missing'])
        return used_letters

    def get_remaining_chars(self) -> set:
        used_letters = self.get_used_chars()
        alphabet = get_alphabet()
        return alphabet - used_letters

    def list_patterns(self) -> tuple:
        return tuple(gp for gp in self.guesses)
