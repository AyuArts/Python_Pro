import asyncio

async def slow_task():
    """
    Імітує виконання завдання протягом 10 секунд.
    """
    await asyncio.sleep(10)
    return "Завдання виконане"

async def main():
    """
    Викликає slow_task() з таймаутом 5 секунд за допомогою asyncio.wait_for().
    Якщо час виконання перевищує 5 секунд, виводить повідомлення про перевищення часу очікування.
    """
    try:
        result = await asyncio.wait_for(slow_task(), timeout=5)
        print(result)
    except asyncio.TimeoutError:
        print("Перевищено час очікування")

# Запуск основної функції
asyncio.run(main())
