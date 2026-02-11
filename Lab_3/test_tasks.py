import math
from tasks import (
    sum_nested_recursive,
    sum_nested_iterative,
    sequence_recursive,
    sequence_iterative
)


def test_sum_nested():
    data = [1, [2, [3, 4, [5]]]]
    assert sum_nested_recursive(data) == 15
    assert sum_nested_iterative(data) == 15


def test_sequence_small_k():
    for k in range(1, 6):
        a1, b1 = sequence_recursive(k)
        a2, b2 = sequence_iterative(k)
        assert math.isclose(a1, a2, rel_tol=1e-9)
        assert math.isclose(b1, b2, rel_tol=1e-9)
