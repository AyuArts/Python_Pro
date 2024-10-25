import time
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

URL = "https://www.w3schools.com/w3images/lights.jpg"
NUM_REQUESTS = 500

def sync_request():
    """
    Синхронне виконання запиту.
    """
    response = requests.get(URL)
    return response.status_code

def run_sync():
    """
    Запускає синхронні запити і вимірює час виконання.
    """
    start_time = time.time()
    for _ in range(NUM_REQUESTS):
        sync_request()
    duration = time.time() - start_time
    print(f"Синхронне виконання зайняло: {duration:.2f} секунд")

def run_multithreading():
    """
    Багатопотокове виконання запитів і вимірювання часу.
    """
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(sync_request, range(NUM_REQUESTS))
    duration = time.time() - start_time
    print(f"Багатопотокове виконання зайняло: {duration:.2f} секунд")

def run_multiprocessing():
    """
    Багатопроцесорне виконання запитів і вимірювання часу.
    """
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        executor.map(sync_request, range(NUM_REQUESTS))
    duration = time.time() - start_time
    print(f"Багатопроцесорне виконання зайняло: {duration:.2f} секунд")

async def async_request(session):
    """
    Асинхронний запит за допомогою aiohttp.
    """
    async with session.get(URL) as response:
        return response.status

async def run_async():
    """
    Асинхронне виконання запитів і вимірювання часу.
    """
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(session) for _ in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)
    duration = time.time() - start_time
    print(f"Асинхронне виконання зайняло: {duration:.2f} секунд")

if __name__ == "__main__":
    # Синхронне виконання
    run_sync()

    # Багатопотокове виконання
    run_multithreading()

    # Багатопроцесорне виконання
    run_multiprocessing()

    # Асинхронне виконання
    asyncio.run(run_async())
