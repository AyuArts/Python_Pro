class ReverseFileIterator:
    """
    Ітератор для читання рядків файлу у зворотному порядку.

    :param file_path: Шлях до файлу, рядки якого потрібно прочитати.
    :type file_path: str
    """
    def __init__(self, file_path: str):
        """
        Ініціалізація ітератора.

        :param file_path: Шлях до файлу, рядки якого потрібно прочитати.
        :type file_path: str
        """
        self.file_path = file_path

    def __iter__(self):
        """
        Ітератор, який повертає рядки файлу у зворотному порядку.

        :return: Ітератор рядків файлу.
        :rtype: iterator
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            # Читаємо всі рядки файлу
            self.lines = file.readlines()[::-1]  # Читання рядків у зворотному порядку
        return iter(self.lines)

# Використання ітератора
file_path = "test_file.log"
for line in ReverseFileIterator(file_path):
    print(line.strip())  # Виводимо рядок без зайвих переносів
