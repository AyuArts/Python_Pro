class Menu:
    """
    Клас для управління головним меню додатку, що дозволяє користувачу виконувати різні дії
    з базою даних фільмів через взаємодію з класом MovieDatabase.

    Атрибути:
        movie_database (MovieDatabase): Об'єкт для управління базою даних фільмів.
        display (Display): Об'єкт для взаємодії з користувачем (ввід/вивід).
    """

    def __init__(self, movie_database, display):
        """
        Ініціалізує екземпляр класу Menu з об'єктами MovieDatabase та Display.

        :param movie_database: Об'єкт для управління базою даних фільмів.
        :type movie_database: MovieDatabase
        :param display: Об'єкт для обробки вводу/виводу користувача.
        :type display: Display
        """
        self.movie_database = movie_database
        self.display = display

    def run(self):
        """
        Запускає головний цикл меню, показуючи опції та обробляючи вибір користувача.
        Дозволяє виконувати різні дії, визначені в конфігурації меню.

        :raises KeyError: Якщо в конфігурації меню відсутні необхідні ключі.
        :return: None
        """
        # Створюємо словник дій, де ключами є вибрані опції, а значеннями — відповідні методи
        actions = {option['key']: option['action'] for option in
                   self.movie_database.menu_options['menus']['main_menu']['options']}

        while True:

            print()

            # Показуємо заголовок головного меню
            self.display.display(self.movie_database.menu_options['menus']['main_menu']['title'])

            # Відображаємо всі доступні опції меню
            for option in self.movie_database.menu_options['menus']['main_menu']['options']:
                self.display.display(f"{option['key']}. {option['option_name']}")


            print()

            # Отримуємо вибір користувача
            choice = self.display.get_input("menu", "choose_action")

            # Якщо користувач вибрав '0', виходимо з меню
            if choice == '0':
                break

            # Отримуємо дію, відповідну вибраному ключу
            action = actions.get(choice)

            if action:
                # Викликаємо метод MovieDatabase відповідно до вибору користувача
                getattr(self.movie_database, action)()
            else:
                # Відображаємо повідомлення про некоректний вибір
                self.display.show_message('menu', 'invalid_choice')
