import logging
from json_loader import load_json


class Display:
    """
    Клас для управління відображенням повідомлень та обробкою вводу користувача.
    Використовується для взаємодії з користувачем через консоль.

    Атрибути:
        logger (logging.Logger): Об'єкт логера для запису повідомлень у консоль.
        messages (dict): Словник з шаблонами повідомлень, завантажених з JSON.
    """

    def __init__(self, messages_file='data/messages_ua.json'):
        """
        Ініціалізує екземпляр класу Display з файлами повідомлень та налаштовує логування.

        :param messages_file: Шлях до JSON-файлу з повідомленнями. За замовчуванням 'messages_ua.json'.
        :type messages_file: str
        """
        self.logger = logging.getLogger('console_logger')
        self.messages = load_json(messages_file)

    def __call__(self, category, message_key):
        """
        Дозволяє викликати об'єкт Display як функцію для отримання вводу користувача.

        :param category: Категорія повідомлення для вводу.
        :type category: str
        :param message_key: Ключ повідомлення для вводу.
        :type message_key: str
        :return: Введені користувачем дані.
        :rtype: str
        """
        return self.get_input(category, message_key)

    def display(self, message):
        """
        Відображає повідомлення в консолі та записує його в лог.

        :param message: Повідомлення для відображення.
        :type message: str
        :return: None
        """
        self.logger.info(message)

    def show_messages(self, messages):
        """
        Відображає список повідомлень у консолі.

        :param messages: Список повідомлень для відображення.
        :type messages: list
        :return: None
        """
        for message in messages:
            self.display(message)

    def show_formatted_messages(self, category, message_key, data_list):
        """
        Форматує та виводить повідомлення з використанням переданих даних.

        :param category: Категорія повідомлення.
        :type category: str
        :param message_key: Ключ повідомлення для форматування.
        :type message_key: str
        :param data_list: Список або кортеж даних для форматування повідомлення.
        :type data_list: list або tuple
        :return: None
        :raises TypeError: Якщо тип `data_list` не підтримується для форматування.
        """
        message_template = self.get_message(category, message_key)

        if isinstance(data_list, tuple):
            # Якщо передано кортеж даних, обробляємо його як один елемент
            self.display(message_template.format(*data_list))
        elif isinstance(data_list, list):
            # Якщо передано список, проходимо по кожному елементу списку
            for data in data_list:
                if isinstance(data, tuple):
                    # Якщо елемент списку — кортеж, розпаковуємо його
                    self.display(message_template.format(*data))
                else:
                    # Якщо елемент списку — рядок, передаємо його як одне значення
                    self.display(message_template.format(data))
        else:
            self.logger.error(f"Непідтримуваний тип даних для форматування: {type(data_list)}")
            raise TypeError(f"Непідтримуваний тип даних для форматування: {type(data_list)}")

    def get_input(self, category, message_key):
        """
        Отримує ввід користувача на основі категорії та ключа повідомлення.

        :param category: Категорія повідомлення для вводу.
        :type category: str
        :param message_key: Ключ повідомлення для вводу.
        :type message_key: str
        :return: Введені користувачем дані або порожній рядок у випадку помилки.
        :rtype: str
        """
        try:
            return input(self.get_message(category, message_key))
        except KeyError:
            self.logger.error(f"Message key '{message_key}' not found in category '{category}'.")
            return ""

    def get_message(self, category, message_key):
        """
        Отримує конкретне повідомлення на основі категорії та ключа з завантажених повідомлень.

        :param category: Категорія повідомлення.
        :type category: str
        :param message_key: Ключ повідомлення.
        :type message_key: str
        :return: Отримане повідомлення або повідомлення за замовчуванням, якщо ключ не знайдено.
        :rtype: str
        """
        category_dict = self.messages.get(category, {})
        return category_dict.get(message_key,
                                 f"Повідомлення для ключа '{message_key}' в категорії '{category}' не знайдено.")

    def show_message(self, category, message_key, *args):
        """
        Відображає повідомлення з підтримкою форматування.

        :param category: Категорія повідомлення.
        :type category: str
        :param message_key: Ключ повідомлення для відображення.
        :type message_key: str
        :param args: Дані для форматування повідомлення.
        :type args: tuple
        :return: None
        """
        message_template = self.get_message(category, message_key)
        if args:
            try:
                message = message_template.format(*args)
            except IndexError as e:
                self.logger.error(f"Помилка форматування повідомлення: {e}")
                message = message_template
        else:
            message = message_template
        self.display(message)
