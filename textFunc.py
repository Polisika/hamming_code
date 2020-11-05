import simple_code_text as sct
import math
from math import factorial as fact
import numpy as np
import sympy as sp


def C(k: int, m: int):
    """Число сочетаний"""
    return fact(m) / (fact(m - k) * fact(k))


def get_key(d, value):
    """Возвращает ключ по значению"""
    for k, v in d.items():
        if v == value:
            return k


def encode(text: list, code: dict):
    """Кодирует текст с проверкой на чётность (каждый третий символ)."""

    quantum = 3  # так как первый вариант
    coded = []
    symbols = []

    for i in range(len(text)):
        # Проверка на четность
        if i % quantum == 0 and i != 0:
            # Вычисление y1 ^ y2 ^ y3
            dig = int(symbols[0])
            for sym in symbols[1:]:
                dig ^= int(sym)

            coded.append(bin(dig)[2:].zfill(len(code[text[i]])))  # Прибавляем y1 ^ y2 ^ y3
            symbols.clear()  # Очищаем буфер

        symbols += text[i]
        coded.append(code[text[i]])

    return coded


def decode(text_coded: list, dict_coded: dict):
    """Декодирует текст с проверкой на четность (каждый 3-ий).
    Возвращает текст и список позиций, в каком блоке ошибка"""
    errors = []
    per = 3     # Сколько символов участвовало в xor
    decoded = []   # Декодированные слова
    codes = []  # Последние per декодированные слова
    coded = dict_coded.values()

    for pos in range(len(text_coded)):
        word = text_coded[pos]
        len_codes = len(codes)

        if len_codes == per:
            xor = int(codes[0], 2)
            for i in range(1, len_codes):
                xor ^= int(codes[i], 2)

            xor = bin(xor)[2:].zfill(len(codes[0]))
            codes.clear()
            if word != xor:
                errors.append(pos)

        elif word in coded:
            decoded += get_key(dict_coded, word)
            codes.append(word)

    return decoded, errors


def hamming_metrics(first: str, second: str):
    """Расстояние Хэмминга между двумя закодированными словами одинаковой длины"""
    if len(first) != len(second):
        raise ValueError("Переданы слова разной длины.")
    return sum([x1 != x2 for x1, x2 in zip(first, second)])


def d0(H: np.ndarray):
    """Количество линейнозависимых столбцов"""
    _, i = sp.Matrix(H.T).T.rref()
    return len(i)


def min_hamming_metrics (dict_coded: dict):
    """Минимальное расстояние Хэмминга между закодированными словами
    Возможна ошибка из-за функции расстояния Хэмминга"""
    list_differences = []
    list_coded = list(dict_coded.values())
    for i, word1 in enumerate(list_coded):
        for word2 in list_coded[i + 1:]:
            list_differences.append(hamming_metrics(word1, word2))

    return min(list_differences)


def hamming_boundary(n: int, k: int, q0: int):
    """Граница Хэмминга - это выражение является нижней границей в том смысле, что оно устанавливает то минимальное
    соотношение корректирующих и информационных разрядов, ниже которого код не может сохранять заданные корректирующие
    способности.
    Возвращает: выполнено ли условие и значение правой части"""
    right = math.log2(sum([C(i, n) for i in range(q0)]))
    return n - k <= right, right


def plotkin_boundary(d_0: int, n: int, k: int):
    """Граница Плоткина, задающая минимальную избыточность, при которой существует помехоустойчивый код, имеющий
    минимальное кодовое расстояние и гарантированно исправляющий q-кратные ошибки
    Возвращает: выполнено ли условие и значение правой части"""
    right = n * 2**(k - 1)/(2**k - 1)
    return n + k >= right if n >= 2*d_0 - 1 else False, right


def varshamov_gilbert_boundary (n: int, k: int, d_0: int):
    """Является нижней границей для числа проверочных разрядов r=n-k в случае кодов большой разрядности, необходимого
    для обеспечения заданного кодового расстояния d_0.
    Возвращает: выполнено ли условие и значение правой части"""
    right = sum([C(i, n - 1) for i in range(0, d_0 - 1)])
    return 2**(n - k) > right, right


def hamming_code(text: list, dict_coded: dict, k: int):
    """
    Кодирование текста с использованием кода Хэмминга.
    :param text текст для кодирования
    :param dict_coded символ и его код
    :param k количество информационных бит
    """
    # keys = list(dict_coded.keys())
    # codes = [x[::-1] for x in list(dict_coded.values())]

    # power_2 = [2**z - 1 for z in range(k - 1, -1, -1)]

    # Добавляем в коды проверочные биты.
    # n = len(codes[0])
    # first = n + k - 2**(k - 1)
    # count = [first]
    # for i in range(0, k - 1):
    #     count.append(power_2[i] - power_2[i+1] - 1)
    #
    # for j in range(len(codes)):
    #     buff = [int(x) for x in list(codes[j])]
    #     res = []
    #     pos = 0
    #     for c in count:
    #         for i in range(c):
    #             res.append(buff[pos])
    #             pos += 1
    #         res.append(sum(res) % 2)
    #     res.reverse()
    #     codes[j] = "".join(str(x) for x in res)

    # Кодируем слова
    # res_dict = dict(zip(keys, codes))
    encoded = []
    for word in text:
        encoded.append(dict_coded[word])

    return encoded


def hamming_decode(code_text: list, dict_coded: dict, H: np.ndarray, k: int):
    """Декодирует последовательность, исправляя ошибки"""

    decoded = []
    err_dict = {}

    for substring in code_text:
        if not(substring in dict_coded.values()):
            v = np.array([int(x) for x in list(substring)])
            # Вычисляем синдром, исправляем одну ошибку
            s = dot_xor(v, H, k)
            err_pos = int("".join([str(x) for x in s]), 2) - 1
            err_dict[substring] = err_pos
            substring = substring[:err_pos] + str(0 if v[err_pos] == 1 else 1) + substring[err_pos + 1:]
        if not (substring in dict_coded.values()):
            decoded.append('e')
        decoded.append(get_key(dict_coded, substring))

    return decoded, err_dict


def dot_xor(v: np.array, H: np.ndarray, k: int):
    syndrome = np.zeros(k, np.int)
    i = 0
    for arr in H:
        dot = arr*v
        e = dot[0]
        for elem in dot[1:]:
            e = e ^ elem
        syndrome[i] = e
        i += 1

    return syndrome


def get_coded_hamming(H: np.ndarray):
    a = []
    for i in range(2 ** 9):
        l = list(bin(i)[2:].zfill(9))
        v = np.array(l, np.int)
        res = dot_xor(v, H, 4)
        if np.array_equal(res, np.zeros(4)):
            a.append(''.join([str(x) for x in v]))
    return dict(zip([str(i) for i in range(len(a))], a))
