import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

# URL для запросов
URL = "https://example.com"


# Асинхронная функция для выполнения запроса с тайм-аутом
async def fetch(session, url):
    try:
        async with session.get(url, timeout=1) as response:
            return await response.text()
    except asyncio.TimeoutError:
        return "Request Timeout"


# Функция для выполнения асинхронных задач в потоке
def thread_task(url, request_count):
    async def run_tasks():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for _ in range(request_count)]
            return await asyncio.gather(*tasks)

    results = asyncio.run(run_tasks())
    return results


# Функция процесса, запускающая несколько потоков
def process_task(url, task_id, request_count):
    print(f"Starting process task {task_id}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(thread_task, url, request_count // 10) for _ in range(10)]
        results = [future.result() for future in futures]
    return results


# Основная функция для запуска процессов и замера времени
if __name__ == '__main__':
    total_requests = 5000
    process_count = 8
    requests_per_process = total_requests // process_count

    start_time = time.time()

    # Создаем процессы и распределяем запросы
    with ProcessPoolExecutor(max_workers=process_count) as executor:
        results = executor.map(process_task, [URL] * process_count, range(process_count),
                               [requests_per_process] * process_count)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Total time for processing {total_requests} requests: {duration:.2f} seconds")
