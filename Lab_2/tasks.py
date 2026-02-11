from itertools import product

from itertools import product

def count_code_words() -> int:
    """
    Возвращает количество допустимых кодовых слов.

    >>> count_code_words()
    192
    """
    first_letters = ('X', 'Y', 'Z')
    other_letters = ('A', 'B', 'C', 'D')

    count = 0
    for first in first_letters:
        for rest in product(other_letters, repeat=3):
            count += 1
    return count

def count_twos_in_ternary() -> int:
    """
    Считает количество цифр '2' в троичной записи числа.

    >>> count_twos_in_ternary()
    3
    """
    value = (9**8) + (3**5) - 9

    digits = []
    while value > 0:
        digits.append(value % 3)
        value //= 3

    return digits.count(2)

def odd_divisors_count(n: int) -> int:
    """
    Возвращает количество различных нечётных делителей числа.

    >>> odd_divisors_count(45)  # 1, 3, 5, 9, 15, 45
    6
    """
    count = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            if d % 2 == 1:
                count += 1
            other = n // d
            if other != d and other % 2 == 1:
                count += 1
        d += 1
    return count


def find_numbers_with_five_odd_divisors() -> list[int]:
    """
    Возвращает список чисел с ровно 5 нечётными делителями.

    >>> find_numbers_with_five_odd_divisors()
    [40000, 41472]
    """
    result = []
    for n in range(40000, 50001):
        if odd_divisors_count(n) == 5:
            result.append(n)
    return result


print(find_numbers_with_five_odd_divisors())
