from loguru import logger
import sys
from pathlib import Path
from typing import Optional, Callable, Union, Any, List
from message_loader import MessageLoader  # Переконайтеся, що цей імпорт коректний


class CustomLogger:
    """
    Клас для кастомного логування з використанням MessageLoader та loguru.
    """

    def __init__(self, message_loader: MessageLoader):
        """
        Ініціалізує CustomLogger, налаштовує логування.

        :param message_loader: Інстанс MessageLoader для завантаження повідомлень.
        """
        self.message_loader = message_loader
        self._configure_logging()

    @staticmethod
    def _conditional_format(record: dict) -> str:
        """
        Кастомний форматтер для логів.

        :param record: Запис лога.
        :return: Відформатована строка лога.
        """
        try:
            time = record["time"].strftime("%Y-%m-%d %H:%M:%S")
            nanoseconds = record["time"].microsecond * 1000  # Перетворюємо мікросекунди в наносекунди
            level = record["level"].name
            file = record["file"].name if record.get("file") else "N/A"
            line = record.get("line", "N/A")
            function = record.get("function", "<module>")
            message = record["message"]
            message_keys = record["extra"].get("message_keys")

            log_parts = [
                f"{time}.{nanoseconds:09d}",
                f"{file}: {line}",
                f"{level}"
            ]

            if function != "<module>":
                log_parts.append(f"{function}")

            if message_keys:
                # Додаємо ключі повідомлень у лог
                keys_str = ".".join(message_keys)
                log_parts.append(f"[{keys_str}]")

            log_parts.append(message)
            return " | ".join(log_parts) + "\n"
        except KeyError as e:
            return f"Помилка форматування лога: відсутній ключ {e}"

    @staticmethod
    def _add_log_handler(
        sink: Union[str, Callable[[str], None]],
        level: Union[str, int],
        log_format: Union[str, Callable[[Any], str]],
        filter_func: Optional[Callable[[Any], bool]] = None,
        colorize: bool = True,
        **kwargs: Any
    ) -> None:
        """
        Універсальна функція для додавання лог-обробників.

        :param sink: Місце, куди відправляється лог (наприклад, sys.stdout або ім'я файлу).
        :param level: Мінімальний рівень логування, починаючи з якого лог буде записуватися.
        :param log_format: Формат виводу повідомлень у лог.
        :param filter_func: Функція для фільтрації повідомлень (за замовчуванням None).
        :param colorize: Увімкнення або вимкнення кольорового форматування (за замовчуванням True).
        """
        logger.add(
            sink,
            level=level,
            format=log_format,
            filter=filter_func,
            colorize=colorize,
            **kwargs
        )

    def _configure_logging(self) -> None:
        """
        Налаштовує систему логування.

        - INFO виводиться на консоль з простим повідомленням.
        - WARNING і вище виводяться на консоль з кастомним форматом.
        - Усі повідомлення рівня DEBUG і вище записуються у файл 'global.log' у директорії логів.
        """
        logger.remove()

        # Получаем текущую директорию и создаём папку для логов
        log_directory = Path().absolute() / f"log_{Path().absolute().name}"
        log_directory.mkdir(parents=True, exist_ok=True)

        global_log_path = str(log_directory / "global.log")

        # Определяем форматы логов
        info_format = "{message}"
        custom_format = self._conditional_format

        # Логирование INFO в консоль
        self._add_log_handler(
            sink=sys.stdout,
            level="INFO",
            log_format=info_format,
            filter_func=lambda record: record["level"].no == logger.level("INFO").no,
            colorize=True
        )

        # Логирование WARNING и выше в консоль
        self._add_log_handler(
            sink=sys.stdout,
            level="WARNING",
            log_format=custom_format,
            colorize=True
        )

        # Логирование всех уровней в файл
        self._add_log_handler(
            sink=global_log_path,
            level="DEBUG",
            log_format=custom_format,
            rotation="10 MB",
            retention="10 days",
            compression="zip",
            colorize=False
        )

        logger.info("Logging configured successfully.")

    def _log(self, level: str, message_keys: Union[List[str], str], *args: Any, **kwargs: Any) -> None:
        """
        Загальний метод для логування повідомлень на будь-якому рівні.

        :param level: Рівень логування (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        :param message_keys: Ключі для отримання повідомлення або саме повідомлення.
        :param args: Додаткові аргументи.
        :param kwargs: Аргументи для форматування повідомлення.
        """
        if isinstance(message_keys, list):
            message = self.message_loader.get_message(message_keys, **kwargs)
            extra = {"message_keys": message_keys}
        else:
            message = message_keys
            extra = {}

        depth = 2  # Фиксированная глубина для логов
        logger.opt(depth=depth).log(level, message, extra=extra)

    def info(self, message_keys: Union[List[str], str], *args: Any, **kwargs: Any) -> None:
        """Логування повідомлень рівня INFO."""
        self._log("INFO", message_keys, *args, **kwargs)

    def error(self, message_keys: Union[List[str], str], *args: Any, **kwargs: Any) -> None:
        """Логування повідомлень рівня ERROR."""
        self._log("ERROR", message_keys, *args, **kwargs)

    def warning(self, message_keys: Union[List[str], str], *args: Any, **kwargs: Any) -> None:
        """Логування повідомлень рівня WARNING."""
        self._log("WARNING", message_keys, *args, **kwargs)

    def debug(self, message_keys: Union[List[str], str], *args: Any, **kwargs: Any) -> None:
        """Логування повідомлень рівня DEBUG."""
        self._log("DEBUG", message_keys, *args, **kwargs)

    def critical(self, message_keys: Union[List[str], str], *args: Any, **kwargs: Any) -> None:
        """Логування повідомлень рівня CRITICAL."""
        self._log("CRITICAL", message_keys, *args, **kwargs)


def get_custom_logger(message_file_name: str) -> CustomLogger:
    """
    Фабрична функція для створення екземпляра CustomLogger.

    :param message_file_name: Назва JSON-файлу з повідомленнями.
    :return: Екземпляр CustomLogger.
    """
    script_dir = Path(__file__).parent
    messages_file_path = script_dir / "data" / message_file_name
    message_loader = MessageLoader(json_file=message_file_name, file_path=str(messages_file_path))
    return CustomLogger(message_loader)
