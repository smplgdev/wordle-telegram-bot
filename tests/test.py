from data.word_dataclass import Word

m = 'match'
mm = 'mismatch'
mi = 'missing'


def test(conceived_word: Word, predicted_word: Word, expected_result: list[str]):
    gp = conceived_word.get_guess_pattern(predicted_word.word)
    got_result = [char.status for char in gp]
    print(f'{expected_result=}\n{got_result=}\n')


if __name__ == '__main__':
    test(Word("ЧЕШКА"), Word("КАЮТА"), [mi, mi, mi, mi, m])
    test(Word("БАГЕТ"), Word("КАТЕТ"), [mi, m, mi, m, m])
    test(Word("БАГЕТ"), Word("КАТЕР"), [mi, m, mm, m, mi])
