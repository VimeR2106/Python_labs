import math

def sum_nested_recursive(data):
    """
    Рекурсивный подсчёт суммы вложенного списка.
    """
    total = 0
    for item in data:
        if isinstance(item, list):
            total += sum_nested_recursive(item)
        else:
            total += item
    return total

def sum_nested_iterative(data):
    """
    Итеративный подсчёт суммы вложенного списка.
    """
    total = 0
    stack = list(data)

    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        else:
            total += item

    return total

def sequence_recursive(k):
    """
    Возвращает (a_k, b_k) рекурсивно.
    """
    if k == 1:
        return 1.0, 1.0

    a_prev, b_prev = sequence_recursive(k - 1)

    a = 0.5 * (math.sqrt(b_prev) + 0.5 * math.sqrt(a_prev))
    b = 1.5 * math.sqrt(b_prev) + 0.5 * a_prev ** 2

    return a, b

def sequence_iterative(k):
    """
    Возвращает (a_k, b_k) итеративно.
    """
    a, b = 1.0, 1.0

    for _ in range(2, k + 1):
        a, b = (
            0.5 * (math.sqrt(b) + 0.5 * math.sqrt(a)),
            1.5 * math.sqrt(b) + 0.5 * a ** 2
        )

    return a, b

print(sum_nested_recursive([1, [2, [3, 4, [5]]]]))
print(sum_nested_iterative([1, [2, [3, 4, [5]]]]))
print(sequence_recursive(10))
print(sequence_iterative(10))
