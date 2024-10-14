import bisect

class User:
    """
    Клас User представляє користувача системи.

    Атрибути:
    ----------
    user_id : int
        Унікальний ідентифікатор користувача.
    name : str
        Ім'я користувача.
    age : int
        Вік користувача.
    """
    def __init__(self, user_id, name, age):
        """
        Ініціалізує нового користувача з унікальним ідентифікатором, ім'ям та віком.

        :param user_id: Унікальний ідентифікатор користувача.
        :type user_id: int
        :param name: Ім'я користувача.
        :type name: str
        :param age: Вік користувача.
        :type age: int
        """
        self.user_id = user_id
        self.name = name
        self.age = age

    def __repr__(self):
        """
        Повертає строкове представлення користувача.

        :return: Строка у вигляді "User(id: {self.user_id}, name: {self.name}, age: {self.age})".
        :rtype: str
        """
        return f"User(id: {self.user_id}, name: {self.name}, age: {self.age})"

    def __lt__(self, other):
        """
        Визначає порівняння користувачів за user_id для сортування.

        :param other: Інший об'єкт User для порівняння.
        :type other: User
        :return: True, якщо поточний user_id менший за user_id іншого користувача.
        :rtype: bool
        """
        return self.user_id < other.user_id


class UserManage:
    """
    Клас UserManage надає методи для керування списком користувачів, включаючи додавання, видалення та сортування.
    """
    def __init__(self):
        """
        Ініціалізує порожній список користувачів та готує змінні для зберігання доступних ID.
        """
        self.users = []  # Список користувачів
        self.next_id = 1
        self.deleted_ids = []  # Список видалених ID

    def get_free_id(self) -> int:
        """
        Повертає вільний ID користувача. Якщо є видалені ID, використовує їх, інакше створює новий.

        :return: Вільний унікальний ID для нового користувача.
        :rtype: int
        """
        if self.deleted_ids:
            return self.deleted_ids.pop(0)
        else:
            free_id = self.next_id
            self.next_id += 1
            return free_id

    def add_user(self, name: str, age: int):
        """
        Додає нового користувача з унікальним ID до списку та сортує список.

        :param name: Ім'я нового користувача.
        :type name: str
        :param age: Вік нового користувача.
        :type age: int
        """
        user_id = self.get_free_id()
        new_user = User(user_id, name, age)
        bisect.insort(self.users, new_user)  # Вставка користувача з автоматичним сортуванням за ID
        self.display_info(f"Користувач {name} доданий з ID: {user_id}")

    def remove_user(self, name: str):
        """
        Видаляє користувача за ім'ям, якщо він існує у списку.

        :param name: Ім'я користувача для видалення.
        :type name: str
        """
        user_to_remove = None
        for user in self.users:
            if user.name == name:
                user_to_remove = user
                break
        if user_to_remove:
            self.users.remove(user_to_remove)
            self.deleted_ids.append(user_to_remove.user_id)
            self.display_info(f"Користувач {name} видалений")
        else:
            self.display_info(f"Користувач {name} не знайдений")

    def get_user_by_name(self, name: str):
        """
        Повертає користувача за ім'ям, якщо він існує у списку.

        :param name: Ім'я користувача для пошуку.
        :type name: str
        :return: Об'єкт користувача або повідомлення про те, що користувача не знайдено.
        :rtype: Union[User, str]
        """
        for user in self.users:
            if user.name == name:
                self.display_info(user)
                return user
        self.display_info(f"Користувач {name} не знайдений")
        return "Користувач не знайдений"

    def get_all_users(self):
        """
        Повертає повний список усіх користувачів.

        :return: Список користувачів.
        :rtype: list
        """
        self.display_info(self.users)

    def display_info(self, message):
        """
        Виводить повідомлення або інформацію на екран.

        :param message: Повідомлення для виведення.
        :type message: str або будь-який об'єкт для виведення.
        """
        print(message)
