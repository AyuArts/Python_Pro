import os
import csv
from PIL import Image


class ImageMetadataIterator:
    """
    Ітератор для збору метаданих про зображення в каталозі.

    :param directory: Шлях до каталогу із зображеннями.
    :type directory: str
    """

    def __init__(self, directory: str):
        """
        Ініціалізує ітератор, встановлюючи шлях до каталогу.

        :param directory: Шлях до каталогу із зображеннями.
        :type directory: str
        """
        self.directory = directory
        self.files = [f for f in os.listdir(directory) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
        self.index = 0

    def __iter__(self):
        """
        Повертає ітератор для проходження по зображеннях у каталозі.

        :return: Ітератор зображень.
        :rtype: iterator
        """
        return self

    def __next__(self):
        """
        Відкриває наступне зображення і витягує його метадані.

        :return: Метадані зображення (ім'я файлу, формат, розмір).
        :rtype: tuple
        """
        if self.index >= len(self.files):
            raise StopIteration

        file_name = self.files[self.index]
        file_path = os.path.join(self.directory, file_name)

        with Image.open(file_path) as img:
            metadata = (file_name, img.format, img.size)

        self.index += 1
        return metadata


def save_metadata_to_csv(directory: str, output_csv: str):
    """
    Зберігає метадані про зображення з каталогу у файл CSV.

    :param directory: Шлях до каталогу із зображеннями.
    :type directory: str
    :param output_csv: Шлях до вихідного файлу CSV.
    :type output_csv: str
    """
    iterator = ImageMetadataIterator(directory)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Format', 'Size'])  # Заголовки CSV

        for metadata in iterator:
            writer.writerow(metadata)


# Використання ітератора для збору метаданих та збереження у файл CSV
image_directory = 'image_test'
output_csv_file = 'image_metadata.csv'

save_metadata_to_csv(image_directory, output_csv_file)
