import aiohttp
import asyncio


async def download_image(url, filename):
    """
    Асинхронна функція для завантаження зображення за URL та збереження його у файл.

    Параметри:
    - url (str): URL зображення для завантаження.
    - filename (str): Ім'я файлу, в який буде збережено зображення.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await response.read())
                print(f"Зображення збережено як {filename}")
            else:
                print(f"Не вдалося завантажити зображення з {url}, статус: {response.status}")


async def main():
    """
    Головна асинхронна функція для керування завданнями завантаження зображень.

    Створює список завдань для завантаження зображень з різних URL-адрес та запускає їх одночасно.
    """
    image_urls = [
        ("https://www.w3schools.com/w3images/lights.jpg", "image1.jpg"),
        ("https://www.w3schools.com/w3images/fjords.jpg", "image2.jpg"),
        ("https://www.w3schools.com/w3images/mountains.jpg", "image3.jpg"),
    ]

    # Створюємо список завдань для завантаження зображень
    tasks = [download_image(url, filename) for url, filename in image_urls]

    # Виконуємо всі завдання одночасно та очікуємо завершення
    await asyncio.gather(*tasks)


# Запускаємо основну функцію
asyncio.run(main())
