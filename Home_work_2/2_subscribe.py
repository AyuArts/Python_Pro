# Task 2

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
