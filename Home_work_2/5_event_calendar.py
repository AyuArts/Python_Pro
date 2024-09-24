# Task 5

events = []


def event_calendar():
    """
    Створює календар подій з можливістю додавання, видалення і перегляду подій.

    Повертає:
    tuple: Функції для додавання, видалення і перегляду подій.
    """

    def add_event(event):
        """
        Додає подію до списку подій.

        Аргументи:
        event (str): Назва події.
        """
        events.append(event)
        print(f"Подію '{event}' додано.")

    def remove_event(event):
        """
        Видаляє подію зі списку подій.

        Аргументи:
        event (str): Назва події.
        """
        if event in events:
            events.remove(event)
            print(f"Подію '{event}' видалено.")
        else:
            print(f"Подію '{event}' не знайдено в списку.")

    def view_events():
        """Виводить список всіх запланованих подій."""
        if events:
            print("Майбутні події:")
            for e in events:
                print(f"- {e}")
        else:
            print("Немає запланованих подій.")

    return add_event, remove_event, view_events


add_event, remove_event, view_events = event_calendar()

add_event("Зустріч з клієнтом о 10:00")
add_event("Презентація проекту о 15:00")

view_events()

remove_event("Зустріч з клієнтом о 10:00")

view_events()