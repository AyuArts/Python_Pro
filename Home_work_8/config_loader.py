# config_loader.py
"""
Модуль для завантаження конфігураційних налаштувань та налаштування логування.

Цей модуль містить функції для:
- Налаштування логування з використанням файлу конфігурації.
- Завантаження основних налаштувань додатку з конфігураційного файлу.
"""

import logging.config
import configparser


def setup_logging(logging_conf_path='config/logging.conf'):
    """
    Налаштовує логування з використанням файлу конфігурації.

    :param logging_conf_path: Шлях до файлу конфігурації логування. За замовчуванням 'data/logging.conf'.
    :type logging_conf_path: str
    :return: Об'єкт логера 'db_logger' для запису повідомлень у лог.
    :rtype: logging.Logger
    :raises FileNotFoundError: Якщо файл конфігурації логування не знайдено за вказаним шляхом.
    :raises KeyError: Якщо в файлі конфігурації відсутній логер 'db_logger'.
    """
    try:
        logging.config.fileConfig(logging_conf_path)
        db_logger = logging.getLogger('db_logger')
        return db_logger
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл конфігурації логування не знайдено: {logging_conf_path}") from e
    except KeyError as e:
        raise KeyError("Логер 'db_logger' не знайдено в конфігураційному файлі логування.") from e


def load_config(config_path='config/settings.conf'):
    """
    Завантажує конфігураційні налаштування з файлу.

    :param config_path: Шлях до конфігураційного файлу. За замовчуванням 'data/settings.conf'.
    :type config_path: str
    :return: Кортеж, що містить назву бази даних, шлях до файлу повідомлень та шлях до файлу меню.
    :rtype: tuple
    :raises FileNotFoundError: Якщо конфігураційний файл не знайдено за вказаним шляхом.
    :raises KeyError: Якщо необхідні секції або ключі відсутні в конфігураційному файлі.
    :raises configparser.NoSectionError: Якщо відсутня необхідна секція в конфігураційному файлі.
    """
    config = configparser.ConfigParser()
    read_files = config.read(config_path)

    if not read_files:
        raise FileNotFoundError(f"Конфігураційний файл не знайдено: {config_path}")

    try:
        # Повертаємо необхідні параметри з конфігураційного файлу
        db_name = config['database']['db_name']
        messages_file = config['files']['messages_file']
        menu_file = config['files']['menu_file']

        return db_name, messages_file, menu_file
    except KeyError as e:
        missing_key = e.args[0]
        raise KeyError(f"В конфігураційному файлі відсутній ключ: {missing_key}") from e
    except configparser.NoSectionError as e:
        missing_section = e.args[0]
        raise configparser.NoSectionError(f"В конфігураційному файлі відсутня секція: {missing_section}") from e
