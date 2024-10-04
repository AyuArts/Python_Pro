import json
import os


class ConfigManager:
    """
    Контекстний менеджер для роботи з JSON конфігураційним файлом.

    :param file_path: Шлях до конфігураційного файлу.
    :type file_path: str
    """

    def __init__(self, file_path: str):
        """
        Ініціалізує контекстний менеджер з шляхом до конфігураційного файлу.

        :param file_path: Шлях до конфігураційного файлу.
        :type file_path: str
        """
        self.file_path = file_path
        self.config = None
        self.original_config = None

    def __enter__(self):
        """
        Автоматично зчитує конфігурацію при вході в контекст.

        :return: Конфігураційні дані як словник.
        :rtype: dict
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
                self.original_config = self.config.copy()  # Зберігаємо оригінал для порівняння
        else:
            self.config = {}

        return self.config

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Автоматично записує зміни в конфігурацію після виходу з контексту, якщо були внесені зміни.

        :param exc_type: Тип винятку.
        :param exc_value: Значення винятку.
        :param traceback: Слідова інформація про виняток.
        """
        if self.config != self.original_config:  # Якщо конфігурація була змінена
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.config, file, indent=4, ensure_ascii=False)
            print(f"Зміни збережено у файл: {self.file_path}")
        else:
            print("Конфігурація не змінювалась, файл не оновлено.")


# Використання контекстного менеджера для зчитування та оновлення конфігурації

config_file = 'config.json'  # Шлях до конфігураційного файлу

with ConfigManager(config_file) as config:
    # Читаємо та змінюємо конфігурацію
    print(f"Поточна конфігурація: {config}")

    # Наприклад, додаємо новий ключ
    config['new_key'] = 'new_value'

    # Якщо потрібно видалити ключ
    if 'old_key' in config:
        del config['old_key']

# При виході з контексту зміни автоматично збережуться у файл
