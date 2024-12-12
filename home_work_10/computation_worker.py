import multiprocessing
import numpy as np
from logs.log_config import get_custom_logger
from typing import List, Union
from functools import reduce
from operator import mul


class MyLogger:
    """
    Клас для управління логуванням.
    """
    logger = get_custom_logger()


def chunk_sum(chunk: np.ndarray) -> Union[float, int]:
    """
    Обчислює суму елементів у переданому чанку.

    :param chunk: Частина великого масиву чисел.
    :return: Сума елементів чанку.
    """
    return np.sum(chunk)


def chunk_factorial(start: int, end: int) -> int:
    """
    Обчислює частковий факторіал на відрізку від start до end.

    :param start: Початкове число для обчислення факторіала.
    :param end: Кінцеве число для обчислення факторіала.
    :return: Факторіал для цього діапазону.
    """
    return reduce(mul, range(start, end + 1), 1)


class ComputationWorker(MyLogger):
    """
    Клас для обчислення суми або факторіала великого числа з використанням паралельної обробки.
    """

    def __init__(self, number: int, operation: str):
        """
        Ініціалізує екземпляр класу ComputationWorker.

        :param number: Число, для якого потрібно обчислити факторіал або суму.
        :param operation: Тип операції ('sum' або 'factorial').
        """
        self.number = number
        self.operation = operation
        self.large_array = self._create_array() if operation == 'sum' else None
        self.num_processes = self._get_num_processes()
        self.chunks = self._create_chunks()

    def _create_array(self) -> np.ndarray:
        """
        Створює великий масив чисел від 1 до `number` включно, якщо операція - сума.

        :return: Великий масив чисел.
        """
        return np.arange(1, self.number + 1)

    @staticmethod
    def _get_num_processes() -> int:
        """
        Визначає кількість доступних процесорів для паралельної обробки.

        :return: Кількість процесорів (не менше 1).
        """
        return max(1, multiprocessing.cpu_count())

    def _create_chunks(self) -> List[Union[np.ndarray, tuple]]:
        """
        Розділяє масив на чанки для кожного процесу (для суми) або розбиває діапазон для обчислення факторіала.

        :return: Список чанків або діапазонів.
        """
        if self.operation == 'sum':
            return np.array_split(self.large_array, self.num_processes)
        elif self.operation == 'factorial':
            chunk_size = self.number // self.num_processes
            ranges = [(i * chunk_size + 1, (i + 1) * chunk_size) for i in range(self.num_processes)]
            ranges[-1] = (ranges[-1][0], self.number)  # Останній відрізок до самого n
            return ranges
        else:
            raise ValueError("Невідома операція. Використовуйте 'sum' або 'factorial'.")

    def create_pool(self) -> Union[float, int]:
        """
        Створює пул процесів та обчислює суму або факторіал паралельно.

        :return: Загальна сума або факторіал числа.
        """
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            if self.operation == "sum":
                func = chunk_sum
                results = pool.map(func, self.chunks)
                total_func = np.sum(results)
            elif self.operation == "factorial":
                func = chunk_factorial
                results = pool.starmap(func, self.chunks)  # starmap дозволяє передавати кілька аргументів
                total_func = reduce(mul, results, 1)
            else:
                raise ValueError("Невідома операція. Використовуйте 'sum' або 'factorial'.")
        return total_func

    def run(self):
        """
        Виконує процес обчислення суми або факторіала на основі вибраної операції.
        """
        try:
            total_func = self.create_pool()
            if self.operation == 'sum':
                self.logger.info(f'Об\'єдна сума: {total_func}')
            elif self.operation == 'factorial':
                self.logger.info(f'Факторіал числа {self.number} дорівнює {total_func}')
            else:
                raise ValueError("Невідома операція. Використовуйте 'sum' або 'factorial'.")
        except Exception as e:
            self.logger.error(f'Сталася помилка: {e}', exc_info=True)


if __name__ == '__main__':
    # Виклик для обчислення суми
    sum_worker = ComputationWorker(10_000_000, 'sum')
    sum_worker.run()

    # Виклик для обчислення факторіала
    factorial_worker = ComputationWorker(1558, 'factorial')
    factorial_worker.run()
