from tasks import is_prime, prime_numbers


def test_is_prime_true():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(29)


def test_is_prime_false():
    assert not is_prime(1)
    assert not is_prime(4)
    assert not is_prime(30)


def test_prime_numbers():
    assert list(prime_numbers(1)) == []
    assert list(prime_numbers(10)) == [2, 3, 5, 7]
    assert list(prime_numbers(30)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert list(prime_numbers(100)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

