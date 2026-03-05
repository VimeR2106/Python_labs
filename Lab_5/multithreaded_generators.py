import time
from threading import Thread
from queue import Queue
from generators import read_file_lines, reverse_words
from pathlib import Path


def multithreaded_generator(filename, max_length=80):
    """
    Многопоточная версия генератора.
    Один поток читает файл, другой обрабатывает строки.
    """
    queue = Queue(maxsize=10)
    
    def reader():
        for line in read_file_lines(filename, max_length):
            queue.put(line)
        queue.put(None)  # Сигнал конца
    
    def processor():
        while True:
            line = queue.get()
            if line is None:
                queue.put(None)
                break
            yield reverse_words(line)
    
    reader_thread = Thread(target=reader, daemon=True)
    reader_thread.start()
    
    processor_gen = processor()
    for result in processor_gen:
        yield result


def create_large_test_file(filename, lines_count=1000):
    """Создаёт большой тестовый файл."""
    lines = [f"line {i}: " + " ".join([f"word{j}" for j in range(10)]) for i in range(lines_count)]
    Path(filename).write_text("\n".join(lines), encoding='utf-8')


def benchmark_single_threaded(filename):
    """Замер времени обычного генератора."""
    start = time.time()
    count = 0
    for line in read_file_lines(filename):
        reverse_words(line)
        count += 1
    elapsed = time.time() - start
    return elapsed, count


def benchmark_multithreaded(filename):
    """Замер времени многопоточного генератора."""
    start = time.time()
    count = 0
    for _ in multithreaded_generator(filename):
        count += 1
    elapsed = time.time() - start
    return elapsed, count


def demo():
    test_file = 'large_test.txt'
    
    print("=== Создание большого тестового файла ===")
    create_large_test_file(test_file, 1000)
    
    print("\n=== Бенчмарк обычного генератора ===")
    elapsed1, count1 = benchmark_single_threaded(test_file)
    print(f"Обработано строк: {count1}")
    print(f"Время: {elapsed1:.4f} сек")
    
    print("\n=== Бенчмарк многопоточного генератора ===")
    elapsed2, count2 = benchmark_multithreaded(test_file)
    print(f"Обработано строк: {count2}")
    print(f"Время: {elapsed2:.4f} сек")
    
    print("\n=== Результаты ===")
    print(f"Обычный генератор: {elapsed1:.4f} сек")
    print(f"Многопоточный: {elapsed2:.4f} сек")
    speedup = elapsed1 / elapsed2 if elapsed2 > 0 else 0
    print(f"Ускорение: {speedup:.2f}x")
    
    Path(test_file).unlink()


if __name__ == "__main__":
    demo()
