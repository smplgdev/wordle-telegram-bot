from random import choice

import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def read_file(char: str):
    arr = list()
    with open(f'nouns/{char}.txt', 'r', encoding='utf8') as f:
        for word in f.readlines():
            word = word.strip().replace('ё', 'е').replace('-', '')
            if len(word) == 5 and word.islower():
                p = morph.parse(word)
                if any({'NOUN', 'nomn', 'sing'} in m.tag for m in p):
                    arr.append(word)

    return list(dict.fromkeys(arr))


def main():
    arr = read_file('summary')
    words_array = set()
    for _ in range(1000):
        words_array.add(choice(arr))

    with open('toconceivewords.txt', 'a', encoding='utf8') as f:
        for word in words_array:
            f.write(word + '\n')
            # 316 words
        # for ord_ in range(1040, 1072):
        #     char = chr(ord_)
        #     arr = read_file(char)
        #     a = range(20) if len(arr) > 20 else range(len(arr))
        #     for word in arr:
        #         f.write(word + '\n')


if __name__ == '__main__':
    # main()
    pass
