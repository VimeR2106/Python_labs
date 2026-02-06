def falling(n, k):
    
    """Рассчитать убывающий факториал от n глубины k.

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    >>> falling(4, 0)
    1
    """
    "*** YOUR CODE HERE ***"
def falling(n, k):
    if k == 0:
        return 0

    fal = 1
    for i in range(k):
        fal *= n - i
    return fal

print(falling(6,3))

def sum_digits(y):
    """Сложить все цифры числа y.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123)
    >>> a
    6
    """
    "*** YOUR CODE HERE ***"
def sum_digits(y):
    sum = 0
    for i in str(y):
        sum += int(i)
    return sum
print(sum_digits(123))



def double_eights(n):
    """Возвращает True если в n есть две цифры 8 подряд.
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    "*** YOUR CODE HERE ***"
def double_eights(n):
    if '88' in str(n):
        return True
    else:
        return False
print(double_eights(808080880))
print(double_eights(234567))
