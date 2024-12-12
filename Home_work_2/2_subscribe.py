import unittest


def subscribe(name):
    """
    Додає підписника, якщо його немає в списку.

    Якщо підписник вже існує, виводиться повідомлення.

    Аргументи:
    name (str): Ім'я підписника.
    """
    if name not in subscribers:
        subscribers.append(name)
    else:
        print(f"{name} вже підписаний.")

    def confirm_subscription():
        """Підтверджує підписку для заданого підписника."""
        print(f"Підписка підтверджена для {name}")

    confirm_subscription()


def unsubscribe(name):
    """
    Видаляє підписника зі списку, якщо він є.

    Якщо підписника немає, виводиться повідомлення про це.

    Аргументи:
    name (str): Ім'я підписника.

    Повертає:
    str: Повідомлення про статус операції.
    """
    if name in subscribers:
        subscribers.remove(name)
        return f"{name} успішно відписаний"
    else:
        return f"{name} даного користувача немає у списку!"


subscribers = []
subscribe("Олена")
subscribe("Ігор")
print(subscribers)

print(unsubscribe("Ігор"))
print(subscribers)


class TestSubscription(unittest.TestCase):

    def setUp(self):
        """Этот метод вызывается перед каждым тестом, чтобы сбросить список подписчиков."""
        global subscribers
        subscribers = []

    def test_subscribe_new_user(self):
        """Тестируем подписку нового пользователя."""
        subscribe("Олена")
        self.assertIn("Олена", subscribers)

    def test_subscribe_existing_user(self):
        """Тестируем попытку подписки уже существующего пользователя."""
        subscribe("Олена")
        with self.assertLogs() as captured:
            subscribe("Олена")
        self.assertIn("Олена вже підписаний.", captured.output[0])

    def test_unsubscribe_existing_user(self):
        """Тестируем отписку существующего пользователя."""
        subscribe("Олена")
        result = unsubscribe("Олена")
        self.assertEqual(result, "Олена успішно відписаний")
        self.assertNotIn("Олена", subscribers)

    def test_unsubscribe_nonexistent_user(self):
        """Тестируем отписку пользователя, которого нет в списке."""
        result = unsubscribe("Ігор")
        self.assertEqual(result, "Ігор даного користувача немає у списку!")

if __name__ == '__main__':
    unittest.main()


