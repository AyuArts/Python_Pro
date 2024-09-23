# Task 5 ==============================================

events = []

def event_calendar():
    def add_event(event):

        events.append(event)
        print(f"Подію '{event}' додано.")

    def remove_event(event):

        if event in events:
            events.remove(event)
            print(f"Подію '{event}' видалено.")
        else:
            print(f"Подію '{event}' не знайдено в списку.")

    def view_events():

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

