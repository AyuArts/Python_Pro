import os

class DirectoryFileIterator:
    """
    Ітератор для проходження через всі файли та підкаталоги в заданому каталозі.

    :param directory: Шлях до каталогу, в якому потрібно проходити по файлах.
    :type directory: str
    """

    def __init__(self, directory: str):
        """
        Ініціалізує ітератор з шляхом до каталогу.

        :param directory: Шлях до каталогу, в якому потрібно проходити по файлах і підкаталогах.
        :type directory: str
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Каталог {directory} не існує")
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"{directory} не є каталогом")

        self.directory = directory
        # Отримуємо всі файли та каталоги
        self.items = os.listdir(directory)
        # Спочатку виділяємо каталоги, потім файли
        self.directories = [f for f in self.items if os.path.isdir(os.path.join(directory, f))]
        self.files = [f for f in self.items if os.path.isfile(os.path.join(directory, f))]
        self.index = 0
        self.is_processing_dirs = True  # Починаємо з каталогів

    def __iter__(self):
        """
        Повертає ітератор для файлів і каталогів у каталозі.

        :return: Ітератор для файлів і каталогів у каталозі.
        :rtype: iterator
        """
        return self

    def __next__(self):
        """
        Повертає наступний файл або каталог у каталозі.
        Спочатку повертає каталоги, потім файли.

        :return: Назва файлу або каталогу та тип (каталог або файл).
        :rtype: tuple
        """
        if self.is_processing_dirs:
            # Повертаємо каталоги
            if self.index >= len(self.directories):
                # Якщо каталоги закінчилися, переходимо до файлів
                self.is_processing_dirs = False
                self.index = 0  # Оновлюємо індекс для файлів
            else:
                dir_name = self.directories[self.index]
                dir_path = os.path.join(self.directory, dir_name)
                dir_size = self.get_directory_size(dir_path)
                size_display = self.format_size(dir_size)
                num_elements = len(os.listdir(dir_path))  # Кількість елементів у каталозі
                self.index += 1
                return dir_name, f"Каталог: {dir_name}, {num_elements} елем., {size_display}"

        if not self.is_processing_dirs:
            # Повертаємо файли
            if self.index >= len(self.files):
                raise StopIteration

            file_name = self.files[self.index]
            file_path = os.path.join(self.directory, file_name)
            file_size_bytes = os.path.getsize(file_path)

            if file_size_bytes == 0:
                file_size = "пустий файл"
            else:
                file_size = self.format_size(file_size_bytes)

            self.index += 1
            return file_name, f"Файл: {file_name} {file_size}"

    def get_directory_size(self, directory: str):
        """
        Обчислює розмір каталогу.

        :param directory: Шлях до каталогу.
        :type directory: str
        :return: Розмір каталогу в байтах.
        :rtype: int
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def format_size(self, size_bytes: int):
        """
        Форматує розмір у зручну для читання одиницю (байти, КБ, МБ).

        :param size_bytes: Розмір у байтах.
        :type size_bytes: int
        :return: Форматований розмір.
        :rtype: str
        """
        if size_bytes >= 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} МБ"
        elif size_bytes >= 1024:
            return f"{size_bytes / 1024:.2f} КБ"
        else:
            return f"{size_bytes} байт"


# Використання ітератора для виведення назв файлів і каталогів

# Запит шляху до каталогу у користувача
directory_path = input("Введіть шлях до каталогу (або залиште порожнім для поточного каталогу): ").strip()

# Якщо шлях не вказано або введено '.', використовуємо поточний каталог
if not directory_path or directory_path == '.':
    directory_path = os.getcwd()
else:
    # Перетворюємо відносний шлях на абсолютний
    if not os.path.isabs(directory_path):
        directory_path = os.path.abspath(directory_path)

# Перевіряємо, чи каталог існує
output_file = os.path.join(directory_path, 'files_info.txt')  # Шлях до файлу для запису

try:
    file_iterator = DirectoryFileIterator(directory_path)

    # Виводимо інформацію про каталоги перед початком ітерації
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Перегляд каталогу: {directory_path}\n\n")  # Записуємо інформацію про каталог у файл
        print(f"Перегляд каталогу: {directory_path}\n")  # Виводимо інформацію на екран

        for result in file_iterator:
            # Виводимо інформацію про файли та каталоги
            info = f"{result[1]}\n"
            print(info.strip())  # Виводимо інформацію на екран
            f.write(info)  # Записуємо інформацію у файл

    print(f"\nІнформацію записано у файл: {output_file}")
except (FileNotFoundError, NotADirectoryError) as e:
    print(e)
