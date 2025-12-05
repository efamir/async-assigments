import asyncio
import random
import string
import time


# Java аналог: CompletableFuture.supplyAsync()
# Цей метод запускає асинхронну задачу, яка нічого не приймає,
# але повертає результат (Supplier). У Python це корутина, яка робить return.
async def generate_chars_async():
    print("Початок генерації масиву...")
    start_time = time.time()

    # Імітація тривалої роботи (як у Java runAsync/supplyAsync)
    await asyncio.sleep(1)

    pool = string.ascii_letters + string.digits + "!@#$%^&*" + " " + "\t"
    generated_array = [random.choice(pool) for _ in range(20)]

    duration = time.time() - start_time
    print(f"[Генерація] Час виконання: {duration:.5f} с")

    return generated_array


# Java аналог: .thenApplyAsync()
# Цей метод викликається ланцюжком після попереднього. Він приймає
# результат попередньої задачі, обробляє його і повертає новий результат.
async def categorize_chars_async(chars):
    print("Початок сортування символів...")
    start_time = time.time()

    await asyncio.sleep(1)

    alpha = []
    spaces = []
    tabs = []
    others = []

    for char in chars:
        if char.isalpha():
            alpha.append(char)
        elif char == ' ':
            spaces.append(char)
        elif char == '\t':
            tabs.append(char)
        else:
            others.append(char)

    duration = time.time() - start_time
    print(f"[Сортування] Час виконання: {duration:.5f} с")

    return chars, alpha, spaces, tabs, others


# Java аналог: .thenAcceptAsync()
# Цей метод приймає результат, виконує дію (наприклад, вивід),
# але нічого не повертає (Void). Це фінальна стадія пайплайну.
async def display_results_async(data):
    print("Виведення результатів на екран...")
    start_time = time.time()

    original, alpha, spaces, tabs, others = data

    readable_original = [c.replace('\t', '\\t') for c in original]
    print(f"\n---> Початковий масив: {readable_original}")

    print(f"---> Алфавітні символи: {alpha}")
    # Краще вивести кількість, бо не видно
    print(f"---> Пробіли (знайдено): {len(spaces)}")
    print(f"---> Табуляції (знайдено): {len(tabs)}")
    print(f"---> Інші символи: {others}\n")

    duration = time.time() - start_time
    print(f"[Вивід] Час виконання: {duration:.5f} с")


# Головна функція
async def main():
    # Ланцюжок викликів (Chaining), як у CompletableFuture:
    # supplyAsync -> thenApplyAsync -> thenAcceptAsync

    raw_chars = await generate_chars_async()
    processed_data = await categorize_chars_async(raw_chars)
    await display_results_async(processed_data)


if __name__ == "__main__":
    asyncio.run(main())
