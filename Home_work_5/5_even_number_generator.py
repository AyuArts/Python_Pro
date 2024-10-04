def even_number_generator():
    """
    Генератор, який генерує нескінченну послідовність парних чисел.

    :yield: Наступне парне число.
    :rtype: int
    """
    num = 0
    while True:
        yield num
        num += 2


class LimitedNumberWriter:
    """
    Менеджер контексту для обмеження кількості згенерованих чисел і запису їх у файл.

    :param file_path: Шлях до файлу для збереження чисел.
    :type file_path: str
    :param limit: Кількість чисел, які потрібно згенерувати та зберегти.
    :type limit: int
    """

    def __init__(self, file_path: str, limit: int):
        """
        Ініціалізує менеджер контексту для збереження парних чисел.

        :param file_path: Шлях до файлу для збереження чисел.
        :type file_path: str
        :param limit: Кількість чисел, які потрібно згенерувати та зберегти.
        :type limit: int
        """
        self.file_path = file_path
        self.limit = limit
        self.generator = None  # Ініціалізуємо генератор пізніше

    def __enter__(self):
        """
        Відкриває файл для запису та ініціалізує генератор парних чисел.

        :return: Менеджер для запису парних чисел.
        :rtype: LimitedNumberWriter
        """
        self.file = open(self.file_path, 'w', encoding='utf-8')
        self.generator = even_number_generator()  # Ініціалізуємо генератор тут
        return self

    def write_numbers(self):
        """
        Генерує та записує парні числа у файл до досягнення обмеження.
        """
        for _ in range(self.limit):
            number = next(self.generator)
            self.file.write(f"{number}\n")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закриває файл після завершення запису.
        """
        self.file.close()


# Використання менеджера контексту для обмеження кількості генерованих чисел і запису їх у файл
file_path = 'even_numbers.txt'
limit = 100  # Обмеження кількості чисел до 100

with LimitedNumberWriter(file_path, limit) as writer:
    writer.write_numbers()
