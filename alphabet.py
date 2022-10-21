def get_alphabet() -> set:
    return set(chr(x) for x in range(1040, 1072))


vowels = ('А', 'О', 'У', 'Е', 'И', 'Ю', 'Я', 'Ы', 'Э')
consonants = ('Н', 'Т', 'С', 'Р', 'В', 'Л', 'К', 'М', 'Д', 'П', 'Ь', 'Г', 'З', 'Б')
rare_chars = ('Ч', 'Й', 'Х', 'Ж', 'Ш', 'Ц', 'Щ', 'Ф', 'Ъ')