"""
Арифметическое кодирование / декодирование.

Предложение: волховал_волхв_в_хлеву_с_волхвами
Кодируем первые 5 символов: «волхо»
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Tuple

TEXT = "волховал_волхв_в_хлеву_с_волхвами"
MESSAGE = TEXT[:5]  # волхо


def trunc4(x: float) -> float:
    """Усечение до 4 знаков после запятой (как в учебном примере)."""
    return int(x * 10000) / 10000


def build_intervals(text: str) -> Tuple[List[str], Dict[str, Tuple[float, float]], Dict[str, int]]:
    """
    Строит таблицу интервалов: символы по убыванию частоты,
    при равенстве — по порядку первого появления в тексте.
    """
    n = len(text)
    counts = Counter(text)
    first_pos: Dict[str, int] = {}
    for i, ch in enumerate(text):
        if ch not in first_pos:
            first_pos[ch] = i

    ordered = sorted(counts.keys(), key=lambda c: (-counts[c], first_pos[c]))

    intervals: Dict[str, Tuple[float, float]] = {}
    cum = 0.0
    for i, ch in enumerate(ordered):
        p = trunc4(counts[ch] / n)
        low = cum
        if i == len(ordered) - 1:
            high = 1.0
        else:
            high = cum + p
        intervals[ch] = (low, high)
        cum = high

    return ordered, intervals, dict(counts)


def encode(
    message: str, intervals: Dict[str, Tuple[float, float]]
) -> Tuple[float, float, List[dict]]:
    """Арифметическое кодирование. Возвращает [low, high) и шаги."""
    low, high = 0.0, 1.0
    steps: List[dict] = []

    for ch in message:
        s_low, s_high = intervals[ch]
        rng = high - low
        new_low = low + rng * s_low
        new_high = low + rng * s_high
        steps.append(
            {
                "symbol": ch,
                "old_low": low,
                "old_high": high,
                "sym_low": s_low,
                "sym_high": s_high,
                "low": new_low,
                "high": new_high,
            }
        )
        low, high = new_low, new_high

    return low, high, steps


def find_symbol(y: float, intervals: Dict[str, Tuple[float, float]]) -> Tuple[str, float, float]:
    for ch, (lo, hi) in intervals.items():
        if lo <= y < hi or (hi >= 1.0 - 1e-12 and lo <= y <= 1.0):
            return ch, lo, hi
    raise ValueError(f"Не найден символ для y={y}")


def decode(
    code: float, intervals: Dict[str, Tuple[float, float]], length: int
) -> Tuple[str, List[dict]]:
    """Арифметическое декодирование length символов."""
    y = code
    decoded: List[str] = []
    steps: List[dict] = []

    for _ in range(length):
        ch, lo, hi = find_symbol(y, intervals)
        width = hi - lo
        y_next = (y - lo) / width
        steps.append(
            {
                "y": y,
                "symbol": ch,
                "sym_low": lo,
                "sym_high": hi,
                "y_next": y_next,
            }
        )
        decoded.append(ch)
        y = y_next

    return "".join(decoded), steps


def main() -> None:
    ordered, intervals, counts = build_intervals(TEXT)
    n = len(TEXT)

    print("=" * 64)
    print(f"Текст ({n} символов): {TEXT}")
    print(f"Сообщение (первые 5): {MESSAGE}")
    print("=" * 64)

    print("\n1. Таблица частот и интервалов")
    print("-" * 64)
    print(f"{'Символ':>8} {'Кол-во':>8} {'p':>10} {'Интервал':>22}")
    for ch in ordered:
        lo, hi = intervals[ch]
        label = "'_'" if ch == "_" else f"'{ch}'"
        print(f"{label:>8} {counts[ch]:>8} {hi - lo:>10.4f}  [{lo:.4f}, {hi:.4f}]")

    print("\n2. Кодирование")
    print("-" * 64)
    print("Формулы:")
    print("  Low_new  = Low_old + (High_old - Low_old) * Low_symbol")
    print("  High_new = Low_old + (High_old - Low_old) * High_symbol")

    low, high, enc_steps = encode(MESSAGE, intervals)
    prefix = ""
    for step in enc_steps:
        prefix += step["symbol"]
        print(f"\n  Символ '{step['symbol']}' → интервал y_{{{prefix}}}:")
        print(
            f"    Low  = {step['old_low']:.5f} + ({step['old_high']:.5f} - {step['old_low']:.5f})"
            f" * {step['sym_low']:.4f} = {step['low']:.6f}"
        )
        print(
            f"    High = {step['old_low']:.5f} + ({step['old_high']:.5f} - {step['old_low']:.5f})"
            f" * {step['sym_high']:.4f} = {step['high']:.6f}"
        )
        print(f"    [{step['low']:.6f}, {step['high']:.6f}]")

    code = 0.14262  # любое число из итогового интервала
    assert low <= code < high

    print(f"\n  Итоговый интервал: [{low:.8f}, {high:.8f}]")
    print(f"  Код: code = {code}")

    print("\n3. Декодирование")
    print("-" * 64)
    print("Формула: y_next = (y - Low_symbol) / (High_symbol - Low_symbol)")

    decoded, dec_steps = decode(code, intervals, len(MESSAGE))
    for i, step in enumerate(dec_steps, 1):
        print(f"\n  Шаг {i}: y = {step['y']:.6f} ∈ [{step['sym_low']:.4f}, {step['sym_high']:.4f}]")
        print(f"         ⇒ символ '{step['symbol']}'")
        print(
            f"         y_next = ({step['y']:.6f} - {step['sym_low']:.4f}) / "
            f"({step['sym_high']:.4f} - {step['sym_low']:.4f}) = {step['y_next']:.6f}"
        )

    print("\n" + "=" * 64)
    print(f"Результат кодирования:  code = {code}")
    print(f"Результат декодирования: «{decoded}»")
    print(f"Проверка: {decoded == MESSAGE}")
    print("=" * 64)


if __name__ == "__main__":
    main()
