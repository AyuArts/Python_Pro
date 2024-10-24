import os
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import mimetypes
from logs.log_config import get_custom_logger


class MyLogger(object):
    """
    Клас для керування логуванням.
    """
    logger = get_custom_logger()


class MyImage(MyLogger):
    """
    Клас для обробки зображень в зазначеній папці.
    Знайдені зображення змінюються до заданого розміру, якщо їх поточний розмір відрізняється.
    """

    def __init__(self, folder_path):
        """
        Ініціалізація об'єкта MyImage.

        :param folder_path: Шлях до папки, в якій знаходяться зображення для обробки.
        """
        super().__init__()
        self.folder_path = folder_path
        os.makedirs(self.folder_path, exist_ok=True)  # Створюємо папку, якщо її немає
        self.image_files = self.find_images()  # Знаходимо зображення під час ініціалізації об'єкта

    def find_images(self):
        """
        Шукає всі зображення в зазначеній папці, виключаючи формати, які не підтримуються Pillow (наприклад, SVG).

        :return: Список файлів зображень у папці.
        """
        image_files = []
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)

            try:
                with Image.open(file_path) as img:
                    img.verify()
                    image_files.append(file_path)
            except (IOError, SyntaxError):
                self.logger.info(f"Файл {filename} не підтримується і буде пропущений.")

        if not image_files:
            self.logger.info(f"У папці {self.folder_path} немає зображень для обробки.")
        else:
            self.logger.info(f"Знайдено {len(image_files)} зображень для обробки.")

        return image_files

    def get_extension(self, url, response):
        """
        Визначає розширення файлу з URL або Content-Type.

        :param url: URL файлу.
        :param response: Об'єкт відповіді requests для отримання заголовків.
        :return: Розширення файлу.
        """
        parsed_url = urlparse(url)
        extension = os.path.splitext(parsed_url.path)[-1]

        if not extension:
            content_type = response.headers.get('Content-Type', '')
            extension = mimetypes.guess_extension(content_type)

        if not extension:
            self.logger.error(f"Не вдалося визначити розширення для URL: {url}")
            return None
        return extension

    def save_file(self, data, file_path, mode='wb'):
        """
        Універсальна функція для збереження даних на диск.

        :param data: Або об'єкт зображення (PIL.Image), або потік даних (для завантаження).
        :param file_path: Шлях для збереження файлу.
        :param mode: Режим відкриття файлу ('wb' для бінарних даних, використовується за замовчуванням).
        """
        try:
            if isinstance(data, Image.Image):
                data.save(file_path)
            else:
                with open(file_path, mode) as f:
                    f.write(data)
            self.logger.info(f"Файл успішно збережений за адресою: {file_path}")
        except Exception as e:
            self.logger.error(f"Помилка при збереженні файлу {file_path}: {e}")

    def download_file(self, url, counter):
        """
        Завантажує файл за URL і зберігає його в папку.

        :param url: URL для завантаження.
        :param counter: Лічильник для унікальної назви файлу.
        :return: Шлях до збереженого файлу або None у разі помилки.
        """
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()  # Перевірка на помилки

                # Отримуємо розширення файлу
                extension = self.get_extension(url, r)
                if not extension:
                    return None

                # Створюємо ім'я файлу
                filename = f"downloaded_file_{counter}{extension}"
                full_path = os.path.join(self.folder_path, filename)

                # Зберігаємо файл через універсальний метод
                self.save_file(r.content, full_path)

                return full_path
        except Exception as e:
            self.logger.error(f"Помилка при завантаженні файлу: {e}")
            return None

    def process_image(self, image_path, width, height):
        """
        Обробляє одне зображення: змінює його розмір і зберігає, якщо це необхідно.

        :param image_path: Шлях до зображення.
        :param width: Нова ширина зображення.
        :param height: Нова висота зображення.
        """
        try:
            with Image.open(image_path) as img:
                self.logger.info(f"Відкрито зображення: {image_path}")

                # Перевірка, чи потрібно змінювати розмір
                if self.is_already_resized(img, width, height):
                    self.logger.info(f"Зображення {image_path} вже має розмір {width}x{height}, пропускаємо обробку.")
                    return

                # Змінюємо розмір зображення
                img = img.resize((width, height))
                self.logger.info(f"Розмір зображення {image_path} змінено на {width}x{height}.")

                # Зберігаємо змінене зображення через універсальний метод
                self.save_file(img, self.create_new_path(image_path))

        except Exception as e:
            self.logger.error(f"Помилка при обробці зображення {image_path}: {e}")

    @staticmethod
    def is_already_resized(image, width, height):
        """
        Перевіряє, чи має зображення вже потрібні розміри.

        :param image: Об'єкт зображення (PIL.Image).
        :param width: Ширина для порівняння.
        :param height: Висота для порівняння.
        :return: True, якщо розміри збігаються, інакше False.
        """
        return image.size == (width, height)

    def create_new_path(self, image_path):
        """
        Створює шлях для збереження нового зображення в папці 'resized_images'.

        :param image_path: Шлях до оригінального зображення.
        :return: Шлях для збереження нового зображення.
        """
        resized_folder = os.path.join(self.folder_path, 'resized_images')
        if not os.path.exists(resized_folder):
            os.makedirs(resized_folder)
        return os.path.join(resized_folder, 'resized_' + os.path.basename(image_path))

    def execute_tasks_in_threads(self, func, args_list, max_threads=4):
        """
        Уніфікована функція для багатопотокового виконання завдань.

        :param func: Функція, яку потрібно виконати в багатопоточному режимі.
        :param args_list: Список аргументів для функції.
        :param max_threads: Максимальна кількість потоків.
        :return: Список результатів виконання завдань.
        """
        self.logger.info(f"Починаємо виконання завдань з функцією {func.__name__}...")

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(func, *args) for args in args_list]
            results = [future.result() for future in futures]

        self.logger.info(f"Завдання з функцією {func.__name__} завершено.")
        return results

    def download_files_in_threads(self, urls, max_threads=4):
        """
        Завантажує файли за URL за допомогою багатопоточності.

        :param urls: Список URL для завантаження.
        :param max_threads: Максимальна кількість потоків.
        :return: Список шляхів до завантажених файлів.
        """
        args_list = [(url, counter) for counter, url in enumerate(urls, start=1)]
        return self.execute_tasks_in_threads(self.download_file, args_list, max_threads)

    def process_images_in_threads(self, width, height, max_threads=4):
        """
        Обробляє всі зображення в папці, використовуючи багатопоточність.

        :param width: Нова ширина для зміни зображень.
        :param height: Нова висота для зміни зображень.
        :param max_threads: Максимальна кількість потоків.
        :return: None
        """
        if not self.image_files:
            self.logger.info("Немає зображень для обробки.")
            return

        # Використовуємо execute_tasks_in_threads для багатопотокової обробки зображень
        args_list = [(image_path, width, height) for image_path in self.image_files]
        self.execute_tasks_in_threads(self.process_image, args_list, max_threads)
        self.logger.info("Обробка зображень завершена.")


if __name__ == '__main__':
    folder_path = './downloads'
    urls = [
        'https://httpbin.org/image/png',
        'https://httpbin.org/image/jpeg',
        'https://httpbin.org/image/svg'
    ]
    width = 800
    height = 800

    # Створюємо об'єкт і завантажуємо зображення
    processor = MyImage(folder_path)
    processor.download_files_in_threads(urls, max_threads=8)  # Завантаження файлів
    processor.process_images_in_threads(width, height, max_threads=4)  # Зміна розміру зображень
