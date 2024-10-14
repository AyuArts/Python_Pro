import pytest
from user_manage import UserManage

@pytest.fixture
def user_manager():
    """
    Фікстура для створення екземпляра UserManage з попередньо доданими користувачами.

    :return: Екземпляр UserManage.
    :rtype: UserManage
    """
    manager = UserManage()
    manager.add_user("Alice", 30)
    manager.add_user("Bob", 25)
    return manager

def test_add_user(user_manager):
    """
    Тестуємо додавання нового користувача.

    :param user_manager: Екземпляр UserManage з попередньо доданими користувачами.
    :type user_manager: UserManage
    """
    user_manager.add_user("Charlie", 40)
    user = user_manager.get_user_by_name("Charlie")
    assert user.name == "Charlie"
    assert user.age == 40

def test_remove_user(user_manager):
    """
    Тестуємо видалення користувача.

    :param user_manager: Екземпляр UserManage з попередньо доданими користувачами.
    :type user_manager: UserManage
    """
    user_manager.remove_user("Alice")
    user = user_manager.get_user_by_name("Alice")
    assert user == "Користувач не знайдений"

def test_get_user_by_name(user_manager):
    """
    Тестуємо отримання користувача за ім'ям.

    :param user_manager: Екземпляр UserManage з попередньо доданими користувачами.
    :type user_manager: UserManage
    """
    user = user_manager.get_user_by_name("Bob")
    assert user.name == "Bob"
    assert user.age == 25

@pytest.mark.skipif(
    len(UserManage().users) < 3,
    reason="Користувачів менше трьох"
)
def test_get_all_users(user_manager):
    """
    Тест, що скипатиметься, якщо користувачів менше трьох.

    :param user_manager: Екземпляр UserManage з попередньо доданими користувачами.
    :type user_manager: UserManage
    """
    users = user_manager.users
    assert len(users) == 3  # Перевіряємо, що є три користувачі
    assert users[0].name == "Alice"
    assert users[1].name == "Bob"
    assert users[2].name == "Charlie"
