import os
import random


def generate_test_data():
    root_dir = "test_data"
    num_files = 1000
    min_size_kb = 1
    max_size_kb = 5

    num_subfolders = 50

    print(f"Генерування в папці '{root_dir}'...")
    print(f"Кількість файлів: {num_files}, Розмір: {min_size_kb}-{max_size_kb} КБ")

    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    existing_dirs = [root_dir]

    for i in range(num_subfolders):
        parent = random.choice(existing_dirs)
        new_folder_name = f"folder_{i}"
        new_path = os.path.join(parent, new_folder_name)

        os.makedirs(new_path, exist_ok=True)
        existing_dirs.append(new_path)

    for i in range(num_files):
        target_dir = random.choice(existing_dirs)
        filename = f"file_{i}.txt"
        filepath = os.path.join(target_dir, filename)

        file_size_bytes = random.randint(min_size_kb * 1024, max_size_kb * 1024)

        with open(filepath, 'wb') as f:
            f.write(os.urandom(file_size_bytes))

        if (i + 1) % 100 == 0:
            print(f"Згенеровано {i + 1} файлів...")

    print("\nГотово! Тестові дані створено.")
    print(f"Шлях для перевірки: {os.path.abspath(root_dir)}")


if __name__ == "__main__":
    generate_test_data()
