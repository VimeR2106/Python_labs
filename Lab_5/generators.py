from functools import reduce
from pathlib import Path


def read_file_lines(filename, max_length=80):
    """
    Генератор для построчного чтения файла.
    Если длина строки больше max_length, возвращает подстроку.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if len(line) > max_length:
                line = line[:max_length]
            yield line


def reverse_words(line):
    """Разворачивает слова в строке."""
    words = line.split()
    reversed_words = words[::-1]
    return ' '.join(reversed_words)


def generate_with_reversed_words(filename, max_length=80):
    """Генератор, который возвращает строки с развёрнутыми словами."""
    for line in read_file_lines(filename, max_length):
        yield reverse_words(line)


def demo_with_map():
    """Демонстрация использования map с генератором."""
    print("=== map: Разворот слов ===")
    lines = ["hello world python", "one two three"]
    result = map(reverse_words, lines)
    for line in result:
        print(line)


def demo_with_filter():
    """Демонстрация использования filter с генератором."""
    print("\n=== filter: Только длинные строки ===")
    lines = ["short", "a very long line here", "tiny"]
    long_lines = filter(lambda x: len(x) > 10, lines)
    for line in long_lines:
        print(line)


def demo_with_reduce():
    """Демонстрация использования reduce."""
    print("\n=== reduce: Конкатенация строк ===")
    lines = ["Hello", "world", "Python"]
    result = reduce(lambda a, b: a + " " + b, lines)
    print(result)


def create_test_file(filename):
    """Создаёт тестовый файл для демонстрации."""
    content = """This is a test file
Short line
Another line with more words in it
Python generator is cool
z a short one"""
    Path(filename).write_text(content, encoding='utf-8')


def demo():
    print("=== Генератор для чтения файла ===")
    
    test_file = 'test_input.txt'
    create_test_file(test_file)
    
    print("\nОригинальные строки (максимум 80 символов):")
    for i, line in enumerate(read_file_lines(test_file), 1):
        print(f"{i}. {line}")
    
    print("\nСтроки с развёрнутыми словами:")
    for i, line in enumerate(generate_with_reversed_words(test_file), 1):
        print(f"{i}. {line}")
    
    demo_with_map()
    demo_with_filter()
    demo_with_reduce()
    
    Path(test_file).unlink()


if __name__ == "__main__":
    demo()
