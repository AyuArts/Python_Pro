# Task 2 ==============================================

def subscribe(name):

    if name not in subscribers:
        subscribers.append(name)
    else:
        print(f"{name} вже підписаний.")

    def confirm_subscription():
        print(f"Підписка підтверджена для {name}")

    confirm_subscription()

def unsubscribe(name):

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
