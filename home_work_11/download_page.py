from random import randint
import asyncio


async def download_page(url):
    """
    Асинхронна функція для симуляції завантаження сторінки.

    Функція приймає URL, затримується на випадковий час від 1 до 5 секунд для
    симуляції завантаження, а потім виводить повідомлення з URL та часом завантаження.

    :param url (str): URL сторінки, яку потрібно "завантажити".
    :return None
    """
    number = randint(1, 5)  # Випадковий час затримки
    await asyncio.sleep(number)
    print(f"URL: {url} - Симульований час завантаження: {number} секунд")


async def main(urls):
    """
    Асинхронна функція для одночасного завантаження декількох сторінок.

    Виконує завантаження сторінок за списком URL-адрес, викликаючи функцію
    download_page для кожного URL у паралельному режимі.

    :param urls (list): Список URL-адрес, які потрібно завантажити.
    :return None
    """
    await asyncio.gather(*(download_page(url) for url in urls))


urls = [
    "https://www.baidu.com",
    "https://example.com",
    "https://jsonplaceholder.typicode.com",
    "https://httpbin.org",
    "https://reqres.in",
]

asyncio.run(main(urls))
