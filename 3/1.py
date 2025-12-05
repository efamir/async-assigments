import time
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor


def get_int(prompt, condition=None, error_message="Некоректне значення."):
    while True:
        try:
            value = int(input(prompt))
            if condition and not condition(value):
                print(error_message)
                continue
            return value
        except ValueError:
            print("Будь ласка, введіть ціле число.")


def get_positive_int():
    return get_int("Введіть кількість рядків (>0): ", lambda x: x > 0, "Кількість має бути більшою за 0.")


def compute_column_sums(matrix_chunk):
    # numpy відпускає GIL, тому потоки працюють паралельно
    return np.sum(matrix_chunk, axis=0)


def main():
    print("Завдання: Сума стовпців матриці")

    # Введення розмірів з перевіркою
    rows = get_positive_int()
    cols = get_positive_int()

    # Введення діапазону генерації чисел
    min_val = get_int("Мінімальне значення елемента: ")
    max_val = get_int(f"Максимальне значення (>= {min_val}): ", lambda x: x >= min_val,
                      "Максимальне значення має бути більшим або рівним за мінімальне.")

    print("\nГенерування матриці...")
    # + 1, бо exclusive
    matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))

    # Вивід матриці
    if rows <= 20 and cols <= 20:
        print("Згенерована матриця:")
        print(matrix)
    else:
        print(f"Матриця {rows}x{cols} занадто велика для повного виводу.")
        print(f"Приклад (верхній лівий кут 10x10):\n{matrix[:10, :10]} ...")

    workers = os.cpu_count() or 4

    # Work Dealing
    print(f"\nWork Dealing ({workers} потоків)")
    start_time = time.time()

    chunk_size = cols // workers
    dealing_chunks = []

    for i in range(workers):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != workers - 1 else cols
        if start < end:
            dealing_chunks.append(matrix[:, start:end])

    dealing_result = None
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(compute_column_sums, dealing_chunks)
        dealing_result = np.concatenate(list(results))

    print(f"Work Dealing результат: {sum(dealing_result)}")
    time_dealing = time.time() - start_time
    print(f"Час: {time_dealing:.5f} сек")

    # Work Stealing
    print("\nWork Stealing (багато дрібних задач)")
    start_time = time.time()

    # Дрібне розбиття для балансування
    n_chunks = workers * 20
    chunk_size = cols // n_chunks if cols // n_chunks > 0 else 1

    stealing_chunks = []
    for i in range(0, cols, chunk_size):
        end = min(i + chunk_size, cols)
        stealing_chunks.append(matrix[:, i:end])

    stealing_result = None
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(compute_column_sums, stealing_chunks)
        stealing_result = np.concatenate(list(results))

    time_stealing = time.time() - start_time
    print(f"Work Stealing результат: {sum(stealing_result)}")
    print(f"Час: {time_stealing:.5f} сек")

    diff = abs(time_dealing - time_stealing)
    winner = "Work Stealing" if time_stealing < time_dealing else "Work Dealing"
    print(f"\nВисновок: {winner} швидше на {diff:.5f} с")


if __name__ == "__main__":
    main()
