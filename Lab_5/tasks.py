
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def prime_numbers(limit):
    numbers = (n for n in range(2, limit + 1)) # Генератор
    return filter(is_prime, numbers)

n = 30
print("Простые числа:", list(prime_numbers(n)))
print("Сумма:", sum(prime_numbers(n)))
