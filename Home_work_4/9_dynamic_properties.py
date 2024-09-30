class DynamicProperties:
    """
    Клас DynamicProperties дозволяє динамічно додавати властивості до екземпляра
    під час виконання програми. Він зберігає значення властивостей у внутрішньому словнику
    і дозволяє отримувати та змінювати ці властивості за допомогою автоматично створених геттерів та сеттерів.
    """

    def __init__(self):
        """
        Ініціалізує об'єкт DynamicProperties і створює внутрішній словник `_properties`
        для зберігання динамічно доданих властивостей.
        """
        self._properties = {}

    def add_property(self, name: str, value: any) -> None:
        """
        Додає нову властивість до об'єкта динамічно.

        Створює геттер і сеттер для динамічної властивості та зберігає її початкове значення
        у внутрішньому словнику `_properties`.

        :param name: Ім'я властивості, яку необхідно додати.
        :param value: Початкове значення властивості.
        """

        # Створюємо геттер, який приймає self
        def getter(self):
            """
            Геттер для динамічної властивості.

            :return: Значення властивості з внутрішнього словника `_properties`.
            """
            return self._properties[name]

        # Створюємо сеттер, який приймає self та значення
        def setter(self, val):
            """
            Сеттер для динамічної властивості.

            Змінює значення властивості у внутрішньому словнику `_properties`.

            :param val: Нове значення властивості.
            """
            self._properties[name] = val

        # Зберігаємо значення в словнику
        self._properties[name] = value

        # Додаємо властивість динамічно за допомогою setattr
        setattr(self.__class__, name, property(getter, setter))


# Використання класу
obj = DynamicProperties()
obj.add_property('name', 'default_name')
print(obj.name)  # default_name
obj.name = "Python"
print(obj.name)  # Python
