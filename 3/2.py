import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_path():
    while True:
        path = input("Введіть шлях до директорії: ")
        if os.path.isdir(path):
            return path
        print("Директорія не знайдена або це не папка.")


def get_positive_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val >= 0:
                return val
            print("Число має бути невід'ємним.")
        except ValueError:
            print("Введіть ціле число.")


def process_file_batch(files, min_size_bytes):
    count = 0
    for file_path in files:
        try:
            if os.path.getsize(file_path) > min_size_bytes:
                count += 1
        except OSError:
            pass
    return count


def main():
    print("Пошук файлів більших за певний розмір")

    directory = get_path()
    size_kb = get_positive_int("Мінімальний розмір файлу (КБ): ")
    min_size_bytes = size_kb * 1024

    print("Індексація файлів...")
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))

    total_files = len(all_files)
    print(f"Всього файлів знайдено: {total_files}")

    if total_files == 0:
        return

    workers = os.cpu_count() or 4

    # Work Dealing
    print(f"\nWork Dealing (розподіл на {workers} частини)")
    start_time = time.time()

    chunk_size = total_files // workers
    dealing_chunks = []

    for i in range(workers):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != workers - 1 else total_files
        if start < end:
            dealing_chunks.append(all_files[start:end])

    count_dealing = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_file_batch, chunk, min_size_bytes) for chunk in dealing_chunks]
        for future in as_completed(futures):
            count_dealing += future.result()

    print(f"Знайдено файлів: {count_dealing}")
    time_dealing = time.time() - start_time
    print(f"Час: {time_dealing:.5f} сек")

    # Work Stealing
    print("\nWork Stealing (пакети по 80 файлів)")
    start_time = time.time()

    batch_size = 80
    stealing_chunks = [all_files[i:i + batch_size] for i in range(0, total_files, batch_size)]

    count_stealing = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_file_batch, chunk, min_size_bytes) for chunk in stealing_chunks]
        for future in as_completed(futures):
            count_stealing += future.result()

    print(f"Знайдено файлів: {count_stealing}")
    time_stealing = time.time() - start_time
    print(f"Час: {time_stealing:.5f} сек")

    diff = abs(time_stealing - time_dealing)
    winner = "Work Stealing" if time_stealing < time_dealing else "Work Dealing"
    print(f"\nВисновок: {winner} швидше на {diff:.5f} с")


if __name__ == "__main__":
    main()
