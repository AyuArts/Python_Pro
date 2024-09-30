class MyList:
    """
    Клас для роботи зі списком, що включає власні реалізації функцій
    len(), sum() та min().
    """

    def __init__(self, items):
        """
        Ініціалізує екземпляр класу MyList.

        :param items: Список елементів (list).
        """
        self.items = items

    def __len__(self):
        """
        Повертає кількість елементів у списку (власна реалізація len()).

        :return: Кількість елементів у списку (int).
        """
        return len(self.items)

    def __iter__(self):
        """
        Повертає ітератор для проходження по елементах списку.

        :return: Ітератор для елементів списку.
        """
        return iter(self.items)

    def __getitem__(self, index):
        """
        Повертає елемент за індексом.

        :param index: Індекс елемента (int).
        :return: Елемент списку.
        """
        return self.items[index]

    def my_len(self):
        """
        Власна реалізація len() без використання вбудованої функції len().

        :return: Кількість елементів у списку (int).
        """
        count = 0
        for _ in self.items:
            count += 1
        return count

    def my_sum(self):
        """
        Власна реалізація sum() без використання вбудованої функції sum().

        :return: Сума елементів у списку (int).
        """
        total = 0
        for item in self.items:
            total += item
        return total

    def my_min(self):
        """
        Власна реалізація min() без використання вбудованої функції min().

        :raises ValueError: Якщо список порожній.
        :return: Найменший елемент у списку.
        """
        if len(self.items) == 0:
            raise ValueError("my_min() arg is an empty sequence")

        minimum = self.items[0]
        for item in self.items[1:]:
            if item < minimum:
                minimum = item
        return minimum


# Тестування функцій
def test_my_list():
    """
    Функція для тестування методів класу MyList.

    :raises AssertionError: Якщо один із тестів не проходить.
    """
    # Створюємо список
    my_list = MyList([5, 3, 8, 6, 2, 10])

    # Тест my_len()
    assert my_list.my_len() == 6, f"Помилка в my_len: {my_list.my_len()}"
    print(f"my_len() працює коректно: {my_list.my_len()}")

    # Тест my_sum()
    assert my_list.my_sum() == 34, f"Помилка в my_sum: {my_list.my_sum()}"
    print(f"my_sum() працює коректно: {my_list.my_sum()}")

    # Тест my_min()
    assert my_list.my_min() == 2, f"Помилка в my_min: {my_list.my_min()}"
    print(f"my_min() працює коректно: {my_list.my_min()}")


# Виклик тестів
test_my_list()
