class FileProcessor:
    """
    Клас для обробки файлів, включаючи запис та читання даних.
    """

    @staticmethod
    def write_to_file(file_path: str, data: str) -> None:
        """
        Записує дані у вказаний файл.

        :param file_path: Шлях до файлу, у який будуть записані дані.
        :type file_path: str
        :param data: Дані для запису.
        :type data: str
        :raises IOError: Якщо виникає помилка при записі у файл.

        :example:
        >>> FileProcessor.write_to_file("example.txt", "Hello, World!")
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
        except IOError as e:
            raise IOError(f"Не вдалося записати у файл {file_path}: {e}")

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """
        Читає дані з вказаного файлу.

        :param file_path: Шлях до файлу, з якого будуть прочитані дані.
        :type file_path: str
        :return: Вміст файлу.
        :rtype: str
        :raises FileNotFoundError: Якщо файл не знайдено.
        :raises IOError: Якщо виникає помилка при читанні файлу.

        :example:
        >>> content = FileProcessor.read_from_file("example.txt")
        >>> print(content)
        Hello, World!
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не знайдено.")
        except IOError as e:
            raise IOError(f"Не вдалося прочитати файл {file_path}: {e}")
