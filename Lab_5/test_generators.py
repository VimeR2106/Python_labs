from pathlib import Path
from generators import (
    read_file_lines,
    reverse_words,
    generate_with_reversed_words,
)


def test_reverse_words():
    """Тест функции разворота слов."""
    assert reverse_words("hello world") == "world hello"
    assert reverse_words("one two three") == "three two one"
    assert reverse_words("single") == "single"
    print("✓ test_reverse_words пройден")


def test_read_file_lines():
    """Тест генератора чтения файла."""
    filename = "test_temp.txt"
    content = "hello world\none two three\nshort"
    Path(filename).write_text(content, encoding='utf-8')
    
    lines = list(read_file_lines(filename))
    assert len(lines) == 3
    assert lines[0] == "hello world"
    assert lines[2] == "short"
    
    Path(filename).unlink()
    print("✓ test_read_file_lines пройден")


def test_read_file_lines_max_length():
    """Тест ограничения по длине строки."""
    filename = "test_temp.txt"
    content = "hello world\none two three\nshort"
    Path(filename).write_text(content, encoding='utf-8')
    
    lines = list(read_file_lines(filename, max_length=5))
    assert lines[0] == "hello"
    assert lines[1] == "one t"
    
    Path(filename).unlink()
    print("✓ test_read_file_lines_max_length пройден")


def test_generate_with_reversed_words():
    """Тест генератора с развёрнутыми словами."""
    filename = "test_temp.txt"
    content = "hello world\none two three\nshort"
    Path(filename).write_text(content, encoding='utf-8')
    
    lines = list(generate_with_reversed_words(filename))
    assert lines[0] == "world hello"
    assert lines[1] == "three two one"
    assert lines[2] == "short"
    
    Path(filename).unlink()
    print("✓ test_generate_with_reversed_words пройден")


def test_generator_is_lazy():
    """Тест, что генератор ленивый (не загружает всё сразу)."""
    filename = "test_temp.txt"
    Path(filename).write_text("test line", encoding='utf-8')
    
    gen = read_file_lines(filename)
    assert hasattr(gen, '__iter__')
    assert hasattr(gen, '__next__')
    
    Path(filename).unlink()
    print("✓ test_generator_is_lazy пройден")


if __name__ == "__main__":
    print("=== Запуск тестов ===")
    test_reverse_words()
    test_read_file_lines()
    test_read_file_lines_max_length()
    test_generate_with_reversed_words()
    test_generator_is_lazy()
    print("\n✓ Все тесты прошли успешно!")
