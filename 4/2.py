import asyncio
import random
import time


# Java аналог: CompletableFuture.supplyAsync()
async def generate_numbers_async():
    print("Початок генерації чисел...")
    start_time = time.time()

    # Імітуємо затримку
    await asyncio.sleep(1)

    # Генеруємо 20 дійсних чисел від -100 до 100
    numbers = [random.uniform(-100, 100) for _ in range(20)]

    duration = time.time() - start_time
    print(f"[Генерація] Час виконання: {duration:.5f} с")

    return numbers


# Java аналог: .thenApplyAsync()
async def calculate_max_diff_async(numbers):
    print("Початок обчислення різниці...")
    start_time = time.time()

    await asyncio.sleep(1)

    # Логіка: max(|a1 - a2|, |a2 - a3|, ...)
    diffs = []
    for i in range(len(numbers) - 1):
        diff = abs(numbers[i] - numbers[i + 1])
        diffs.append(diff)

    result = max(diffs)

    duration = time.time() - start_time
    print(f"[Обчислення] Час виконання: {duration:.5f} с")

    return numbers, result


# Java аналог: .thenAcceptAsync()
async def display_result_async(data):
    print("Виведення результатів...")
    start_time = time.time()

    numbers, result_value = data

    formatted_nums = [round(num, 2) for num in numbers]

    print(f"\n---> Початковий масив (перші 5): {formatted_nums[:5]} ...")
    print(f"---> Максимальна різниця модулів сусідів: {result_value:.5f}\n")

    duration = time.time() - start_time
    print(f"[Вивід] Час виконання: {duration:.5f} с")


async def main():
    # Ланцюжок виконання
    # 1. Отримати дані (supply)
    numbers = await generate_numbers_async()

    # 2. Обробити дані (apply)
    processed_data = await calculate_max_diff_async(numbers)

    # 3. Вивести результат (accept)
    await display_result_async(processed_data)


if __name__ == "__main__":
    asyncio.run(main())
