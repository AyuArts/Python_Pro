class Person:
    """
    Клас для представлення людини з іменем та віком.
    Підтримує порівняння людей за віком і сортування списку об'єктів.
    """

    def __init__(self, name, age):
        """
        Ініціалізує екземпляр класу Person.

        :param name: Ім'я людини (str).
        :param age: Вік людини (int).
        """
        self.name = name
        self.age = age

    def __lt__(self, other):
        """
        Порівнює двох людей за віком (менше).

        :param other: Інший екземпляр класу Person.
        :return: True, якщо вік поточної людини менший, інакше False.
        """
        return self.age < other.age

    def __eq__(self, other):
        """
        Порівнює двох людей за віком (рівність).

        :param other: Інший екземпляр класу Person.
        :return: True, якщо вік людей рівний, інакше False.
        """
        return self.age == other.age

    def __gt__(self, other):
        """
        Порівнює двох людей за віком (більше).

        :param other: Інший екземпляр класу Person.
        :return: True, якщо вік поточної людини більший, інакше False.
        """
        return self.age > other.age

    def __repr__(self):
        """
        Повертає строкове представлення об'єкта Person.

        :return: Строкове представлення об'єкта (str).
        """
        return f"Person(name='{self.name}', age={self.age})"

    @staticmethod
    def sort_people(people):
        """
        Сортує список об'єктів Person за віком за допомогою алгоритму сортування бульбашкою.

        :param people: Список об'єктів Person для сортування.
        :return: None. Список людей буде відсортований на місці.
        """
        n = len(people)
        for i in range(n):
            for j in range(0, n - i - 1):
                if people[j] > people[j + 1]:  # Використовуємо __gt__ для порівняння
                    people[j], people[j + 1] = people[j + 1], people[j]


# Приклад використання:
people = [
    Person("Alice", 30),
    Person("Bob", 25),
    Person("Charlie", 35),
    Person("David", 28)
]

# Викликаємо метод сортування без додаткових функцій
Person.sort_people(people)

# Виводимо відсортований список
print(people)
