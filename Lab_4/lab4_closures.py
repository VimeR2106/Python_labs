from functools import update_wrapper
from json import JSONDecodeError, loads
from time import monotonic, sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class RateLimiter:
    """Простой декоратор-класс для ограничения частоты вызовов."""

    def __init__(self, func=None, *, calls=1, period=1.0):
        if calls < 1:
            raise ValueError("calls must be >= 1")
        if period <= 0:
            raise ValueError("period must be > 0")

        self.func = func
        self.calls = calls
        self.period = period
        self.timestamps = []
        self.recursion_depth = 0

        if func is not None:
            update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        # Режим декорирования: @RateLimiter(calls=..., period=...)
        if self.func is None:
            if not args or not callable(args[0]):
                raise TypeError("Decorator expects a callable")
            return RateLimiter(args[0], calls=self.calls, period=self.period)

        # Для рекурсии ограничение применяем только к верхнему вызову.
        if self.recursion_depth == 0:
            self._wait_if_needed()
            self.timestamps.append(monotonic())

        self.recursion_depth += 1
        try:
            return self.func(*args, **kwargs)
        finally:
            self.recursion_depth -= 1

    def _wait_if_needed(self):
        now = monotonic()
        self.timestamps = [t for t in self.timestamps if now - t < self.period]

        if len(self.timestamps) >= self.calls:
            wait_time = self.period - (now - self.timestamps[0])
            if wait_time > 0:
                sleep(wait_time)


def make_api_text_fetcher(
    api_url,
    *,
    timeout=5.0,
    calls=1,
    period=1.0,
):
    """Возвращает замыкание для получения текста из API."""

    @RateLimiter(calls=calls, period=period)
    def fetch_text():
        request = Request(api_url, headers={"User-Agent": "Python-Lab-4"})
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError, JSONDecodeError, UnicodeDecodeError) as error:
            return f"API error: {error}"

        if isinstance(payload, dict):
            data = payload.get("data", [])
            if data and isinstance(data[0], dict):
                attributes = data[0].get("attributes", {})
                body = attributes.get("body")
                if isinstance(body, str) and body.strip():
                    return body

        return "API response format is unexpected"

    return fetch_text


@RateLimiter
def ping(name="pong"):
    return f"ping: {name}"


@RateLimiter(calls=2, period=1.0)
def factorial(n):
    if n < 2:
        return 1
    return n * factorial(n - 1)


def demo():
    print("=== Демонстрация декоратора-класса ===")
    print(ping())

    print("\n=== Демонстрация рекурсии ===")
    print("factorial(6) =", factorial(6))
    print("factorial(7) =", factorial(7))

    print("\n=== Замыкание для API dogapi.dog ===")
    fetch_dog_fact = make_api_text_fetcher(
        "https://dogapi.dog/api/v2/facts",
        calls=1,
        period=1.0,
    )
    print("fact #1:", fetch_dog_fact())
    print("fact #2:", fetch_dog_fact())


if __name__ == "__main__":
    demo()
