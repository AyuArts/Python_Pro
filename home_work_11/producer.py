import asyncio

async def producer(queue):
    """
    Асинхронна функція, що створює елементи і додає їх у чергу.

    Параметри:
    queue (asyncio.Queue): черга, в яку будуть додаватися елементи.

    Логіка:
    - Створює 5 елементів, кожен з яких додається в чергу з інтервалом у 1 секунду.
    - Після завершення створення елементів додає значення None як сигнал завершення для споживача.
    """
    for i in range(5):
        await asyncio.sleep(1)
        await queue.put(i)
        print(f"Produced {i}")
    await queue.put(None)  # Сигнал для завершення consumer

async def consumer(queue):
    """
    Асинхронна функція, що споживає елементи з черги.

    Параметри:
    queue (asyncio.Queue): черга, з якої будуть вилучатися елементи.

    Логіка:
    - Працює в циклі, отримуючи елементи з черги.
    - Виводить значення елемента на екран.
    - Якщо отримує значення None, завершує роботу.
    """
    while True:
        await asyncio.sleep(2)
        item = await queue.get()
        if item is None:  # Перевірка сигналу для завершення
            break
        print(f"Consumed {item}")
        queue.task_done()

async def main():
    """
    Основна асинхронна функція для ініціалізації черги та запуску завдань продюсера і споживача.

    Логіка:
    - Створює екземпляр asyncio.Queue.
    - Запускає одночасне виконання функцій producer і consumer за допомогою asyncio.gather.
    """
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

# Запуск основної функції main
asyncio.run(main())
