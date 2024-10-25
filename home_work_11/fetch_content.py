import aiohttp
import asyncio


async def fetch_content(url: str) -> str:
    """
    Асинхронна функція, яка виконує HTTP-запит до вказаного URL і повертає вміст сторінки.
    У разі помилки підключення повертає повідомлення про помилку.

    :param url (str): URL сторінки, яку потрібно завантажити.
    :return str: Вміст сторінки або повідомлення про помилку.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Піднімає виключення для статус-кодів 4xx/5xx
                html = await response.text()
                return f"URL: {url}\nСтатус: {response.status}\nВміст: {html[:50]}..."
    except aiohttp.ClientError as e:
        return f"Помилка при завантаженні {url}: {str(e)}"


async def fetch_all(urls: list) -> None:
    """
    Асинхронна функція для завантаження вмісту декількох сторінок одночасно.

    Виконує завантаження сторінок за списком URL-адрес, викликаючи функцію fetch_content
    для кожного URL у паралельному режимі. Виводить вміст або повідомлення про помилку.

    :param urls (list): Список URL-адрес, які потрібно завантажити.
    :return None
    """
    results = await asyncio.gather(*(fetch_content(url) for url in urls))
    for result in results:
        print(result)


urls = [
    "https://www.baidu.com",
    "https://example.com",
    "https://jsonplaceholder.typicode.com",
    "https://httpbin.org",
    "https://reqres.in",
]

asyncio.run(fetch_all(urls))
