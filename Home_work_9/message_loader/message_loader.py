import os
import json
import inspect
import logging
from typing import List

class MessageLoader:
    """
    Класс для завантаження та отримання повідомлень із JSON-файлу.

    Використовується патерн Singleton, що забезпечує створення одного екземпляра класу для кожного
    шляху до файлу, незалежно від кількості викликів.
    """
    _instances = {}

    def __new__(cls, json_file: str, file_path: str = None):
        """
        Створює новий екземпляр класу або повертає існуючий для конкретного шляху до файлу.
        """
        if file_path is None:
            frame = inspect.currentframe()
            try:
                outer_frames = inspect.getouterframes(frame)
                caller_frame = outer_frames[2] if len(outer_frames) >= 3 else outer_frames[1]
                caller_dir = os.path.dirname(os.path.abspath(caller_frame.filename))
                file_path = os.path.join(caller_dir, 'data', json_file)
            finally:
                del frame
        else:
            file_path = os.path.abspath(file_path)

        if file_path not in cls._instances:
            instance = super(MessageLoader, cls).__new__(cls)
            instance._messages = None
            instance._file_path = file_path
            cls._instances[file_path] = instance
        return cls._instances[file_path]

    def load_messages(self) -> dict:
        """
        Завантажує повідомлення з JSON-файлу, якщо вони ще не завантажені.
        """
        if self._messages is None:
            if not os.path.exists(self._file_path):
                raise FileNotFoundError(f"Файл з повідомленнями не знайдено: {self._file_path}")
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self._messages = json.load(f)
                self._validate_json_structure()
        return self._messages

    def _validate_json_structure(self):
        """
        Валідує структуру JSON-файлу для забезпечення коректності даних.
        """
        if not isinstance(self._messages, dict):
            raise ValueError("Неправильна структура JSON: очікується словник на верхньому рівні.")

    def get_message(self, keys: List[str], **kwargs) -> str:
        """
        Отримує повідомлення за заданими ключами з можливістю форматування.
        """
        messages = self.load_messages()
        msg = messages
        for key in keys:
            msg = msg.get(key)
            if msg is None:
                logging.error(f"Ключ '{key}' не знайдено у повідомленнях.")
                return "Повідомлення не знайдено."

        try:
            return msg.format(**kwargs)
        except KeyError as e:
            logging.error(f"Неможливо відформатувати повідомлення: відсутній ключ {e}.")
            return "Помилка форматування повідомлення."

    def reset_cache(self):
        """
        Скидає кеш повідомлень, змушуючи перезавантажити їх із файлу при наступному виклику.
        """
        self._messages = None
        logging.info("Кеш повідомлень скинуто.")
