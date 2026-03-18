import time
import requests
from functools import wraps

########### Декоратор для ограничения количества вызовов ##########
def rate_limiter(func=None, *, max_calls=2, period=5):
    calls = []
    recursion_flag = [False]

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal calls
            now = time.time()
            # Только для внешнего вызова
            if not recursion_flag[0]:
                calls = [t for t in calls if now - t < period]
                if len(calls) >= max_calls:
                    print("Лимит вызовов превышен, попробуйте позже")
                    return None
                calls.append(now)
                recursion_flag[0] = True
                result = f(*args, **kwargs)
                recursion_flag[0] = False
                return result
            else:
                # Внутренние рекурсивные вызовы не лимитируем
                return f(*args, **kwargs)
        return wrapper

    if func is None:
        return decorator
    return decorator(func)

########## Получение данных с API ##########
def make_fetcher(url):
    """
    Замыкание для получения данных с API.

    Возвращает функцию, которая делает запрос и
    возвращает текст ответа.
    """
    def fetch():
        try:
            response = requests.get(url)
            data = response.json()

            # Пытаемся взять текст из разных полей
            attributes = data["data"][0]["attributes"]
            return attributes.get("body") or attributes.get("text")

        except Exception as e:
            return f"Ошибка: {e}"

    return fetch

########## Функции собак и рекурсий ##########
@rate_limiter(max_calls=1000, period=10000000000)
def get_dog_fact():
    """
    Получает случайный факт о собаке через API.
    Использует замыкание make_fetcher.
    """
    fetch = make_fetcher("https://dogapi.dog/api/v2/facts")
    return fetch()

# Проверка работы

# Пример рекурсии
@rate_limiter(max_calls=1, period=0.000000001)
def factorial(n):
    """
    Пример рекурсивной функции с декоратором.
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)

########## Основной запуск ##########
if __name__ == "__main__":
    print("--- Dog facts ---")
    for i in range(4):
        print(f"Fact {i+1}:", get_dog_fact())
        time.sleep(1)

    print("\n--- Factorials ---")
    for i in range(3, 8):
        print(f"factorial({i}) =", factorial(i))
        time.sleep(1)