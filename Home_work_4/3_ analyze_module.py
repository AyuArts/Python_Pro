import inspect
import importlib


def analyze_module(module_name, _func, _class, doc=True):
    """
    Аналізує модуль, виводячи всі функції, їхні сигнатури, класи та документацію.

    :param module_name: Назва модуля у вигляді рядка
    :param doc: Якщо True, виводиться документація для кожної функції та класу.
    """
    try:
        # Імпортуємо модуль за його назвою
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Модуль '{module_name}' не знайдено.")
        return

    print(f"Модуль: {module_name}\n")

    # Отримуємо всі члени модуля
    members = inspect.getmembers(module)

    def print_documentation(obj, doc):
        """
        Виводить документацію для об'єкта, якщо doc=True.

        :param obj: Об'єкт (функція або клас), для якого треба вивести документацію
        :param doc: Якщо True, виводиться документація
        """
        if doc:
            documentation = inspect.getdoc(obj) or "(немає документації)"
            print(f"  Документація: {documentation}")

    if _func:
        # Функції (включаємо вбудовані функції)
        functions = [member for member in members if inspect.isfunction(member[1]) or inspect.isbuiltin(member[1])]
        print("Функції:")
        if functions:
            for name, func in functions:
                try:
                    sig = inspect.signature(func)
                except ValueError:
                    sig = "(не вдалося отримати сигнатуру)"

                print(f"- {name}{sig}")
                # Викликаємо функцію для виведення документації
                print_documentation(func, doc)
        else:
            print("- <немає функцій у модулі>")

    if _class:
        # Класи
        classes = [member for member in members if inspect.isclass(member[1])]
        print("\nКласи:")
        if classes:
            for name, cls in classes:
                print(f"- {name}")
                # Викликаємо функцію для виведення документації
                print_documentation(cls, doc)
        else:
            print("- <немає класів у модулі>")


# Приклад використання
analyze_module("math", _func=True, _class=True, doc=False)
