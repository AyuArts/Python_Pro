import sqlite3
import datetime
from contextlib import closing
import os
from json_loader import load_json  # Імпортуємо функцію завантаження JSON
from config_loader import setup_logging, load_config

# Ініціалізація логування
db_logger = setup_logging()

# Завантаження налаштувань конфігурації
global_db_name, global_messages_file, global_menu_file = load_config()


class MovieDatabase:
    """
    Клас для управління операціями з базою даних, пов'язаними з фільмами та акторами.
    Підтримує CRUD операції для фільмів та акторів, а також різноманітні запити та звіти.

    Attributes:
        db_name (str): Назва файлу SQLite бази даних.
        messages (dict): Словник з шаблонами повідомлень, завантажених з JSON.
        menu_options (dict): Словник з опціями меню, завантажених з JSON.
        display (Display): Об'єкт для взаємодії з користувачем (ввід/вивід).
    """

    def __init__(self, db_name=global_db_name, messages_file=global_messages_file, menu_file=global_menu_file,
                 display=None):
        """
        Ініціалізує екземпляр MovieDatabase з назвою бази даних, повідомленнями,
        опціями меню та об'єктом display для взаємодії з користувачем.

        :param db_name: Назва файлу SQLite бази даних. За замовчуванням global_db_name.
        :type db_name: str
        :param messages_file: Шлях до JSON-файлу з повідомленнями. За замовчуванням global_messages_file.
        :type messages_file: str
        :param menu_file: Шлях до JSON-файлу з опціями меню. За замовчуванням global_menu_file.
        :type menu_file: str
        :param display: Об'єкт для обробки вводу/виводу користувача. За замовчуванням None.
        :type display: Display, опціонально
        """
        self.db_name = db_name
        self.messages = load_json(messages_file)
        self.menu_options = load_json(menu_file)
        self.display = display  # Зберігаємо об'єкт Display як атрибут класу

    def get_message(self, category, key):
        """
        Отримує конкретне повідомлення на основі категорії та ключа з завантажених повідомлень.

        :param category: Категорія повідомлення.
        :type category: str
        :param key: Ключ, що ідентифікує конкретне повідомлення.
        :type key: str
        :return: Отримане повідомлення або повідомлення за замовчуванням, якщо ключ не знайдено.
        :rtype: str
        """
        return self.messages.get(category, {}).get(key,
                                                   f"Повідомлення для ключа '{key}' не знайдено в категорії '{category}'")

    @staticmethod
    def movie_age(year):
        """
        Обчислює вік фільму на основі року випуску.

        :param year: Рік випуску фільму.
        :type year: int
        :return: Вік фільму.
        :rtype: int
        """
        current_year = datetime.datetime.now().year
        return current_year - year

    def execute_script(self, script_name_or_filenames, params=(), fetch=False):
        """
        Виконує один або декілька SQL-скриптів з каталогу 'sql_scripts'.

        :param script_name_or_filenames: Назва одного SQL-скрипта або список назв скриптів.
        :type script_name_or_filenames: str або list
        :param params: Параметри для передачі в SQL-скрипт. За замовчуванням ().
        :type params: tuple, опціонально
        :param fetch: Чи потрібно отримувати та повертати результати. За замовчуванням False.
        :type fetch: bool, опціонально
        :return: Отримані результати або ID останнього вставленого рядка, залежно від параметра 'fetch'.
        :rtype: Any
        """
        if isinstance(script_name_or_filenames, list):
            # Виконуємо кілька скриптів
            for filename in script_name_or_filenames:
                script_path = os.path.join('sql_scripts', filename)
                with open(script_path, 'r', encoding='utf-8') as file:
                    script = file.read()
                self.execute_query(script)
        else:
            # Виконуємо один скрипт
            script_path = os.path.join('sql_scripts', script_name_or_filenames)
            with open(script_path, 'r', encoding='utf-8') as file:
                query = file.read()
            return self.execute_query(query, params, fetch)

    def execute_query(self, query, params=(), fetch=False):
        """
        Виконує окремий SQL-запит з опціональними параметрами та можливістю отримання результатів.

        :param query: SQL-запит для виконання.
        :type query: str
        :param params: Параметри для передачі в SQL-запит. За замовчуванням ().
        :type params: tuple, опціонально
        :param fetch: Чи потрібно отримувати та повертати результати. За замовчуванням False.
        :type fetch: bool, опціонально
        :return: Отримані результати або ID останнього вставленого рядка, залежно від параметра 'fetch'.
        :rtype: Any
        """
        return self._execute_with_cursor(lambda cursor: self._execute_and_fetch(cursor, query, params, fetch))

    def _execute_with_cursor(self, operation):
        """
        Виконує операцію з використанням курсора бази даних, забезпечуючи коректне закриття з'єднання.

        :param operation: Функція, яка приймає курсор і виконує певну операцію.
        :type operation: callable
        :return: Результат виконання функції 'operation'.
        :rtype: Any
        """
        with closing(sqlite3.connect(self.db_name)) as conn:
            with closing(conn.cursor()) as cursor:
                result = operation(cursor)
                conn.commit()
                return result

    @staticmethod
    def _execute_and_fetch(cursor, query, params, fetch):
        """
        Виконує SQL-запит та, за потреби, отримує результати.

        :param cursor: Курсор бази даних.
        :type cursor: sqlite3.Cursor
        :param query: SQL-запит для виконання.
        :type query: str
        :param params: Параметри для передачі в SQL-запит.
        :type params: tuple
        :param fetch: Чи потрібно отримувати та повертати результати.
        :type fetch: bool
        :return: Отримані результати або ID останнього вставленого рядка.
        :rtype: Any
        """
        db_logger.debug(f"Виконання запиту: {query} з параметрами: {params}")
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            db_logger.debug(f"Результат запиту: {result}")
            return result
        return cursor.lastrowid

    def create_tables(self):
        """
        Створює необхідні таблиці в базі даних, виконавши відповідні SQL-скрипти.
        """
        self.execute_script(['create_movies_table.sql', 'create_actors_table.sql', 'create_movie_cast_table.sql'])

    def get_all_actors(self):
        """
        Уніфікований метод для отримання списку всіх акторів.

        :return: Список акторів з бази даних.
        :rtype: list
        """
        return self.execute_script('get_all_actors.sql', fetch=True)

    def add_movie(self):
        """
        Додає новий фільм до бази даних, отримуючи інформацію від користувача.
        Після додавання фільму пропонує вибрати акторів для прив'язки до фільму.

        :return: None
        """
        # Получаем информацию о фильме от пользователя
        title = self.display.get_input("movie_input", "enter_movie_title")
        release_year_input = self.display.get_input("movie_input", "enter_release_year")

        try:
            release_year = int(release_year_input)
        except ValueError:
            self.display.show_message("messages", "invalid_choice")
            return

        genre = self.display.get_input("movie_input", "enter_genre")

        # Вставляем фильм в базу данных и получаем его идентификатор
        movie_id = self.execute_script('insert_movie.sql', (title, release_year, genre))

        # Сообщаем об успешном добавлении фильма
        self.display.show_message("messages", "movie_added_success")

        # Теперь предлагаем выбрать актёров для этого фильма
        self.add_actors_to_movie(movie_id)

    def add_actors_to_movie(self, movie_id):
        """
        Додає акторів до фільму після його створення.

        :param movie_id: Ідентифікатор фільму.
        :return: None
        """
        # Получаем список всех доступных актёров
        actors = self.get_all_actors()

        if not actors:
            self.display.show_message("messages", "no_actors_available")
            return

        # Показываем список актёров
        self.display.display("Оберіть акторів для фільму:")
        for idx, actor in enumerate(actors, 1):
            self.display.display(f"ID: {actor[0]}, Ім'я: {actor[1]}")

        # Позволяем пользователю выбрать актёров
        selected_actors = self.display.get_input("actor", "choose_actors")

        # Преобразуем ввод пользователя в список индексов
        try:
            selected_indices = list(map(int, selected_actors.split(',')))
        except ValueError:
            self.display.show_message("messages", "invalid_choice")
            return

        # Проверяем, что все выбранные индексы соответствуют существующим ID
        valid_actor_ids = {actor[0] for actor in actors}
        invalid_ids = [idx for idx in selected_indices if idx not in valid_actor_ids]

        if invalid_ids:
            self.display.show_message("messages", "invalid_actor_ids", ", ".join(map(str, invalid_ids)))
            return

        # Связываем выбранных актёров с фильмом
        for actor_id in selected_indices:
            self.execute_script('link_actor_to_movie.sql', (movie_id, actor_id))

        self.display.show_message("messages", "actors_added_to_movie")

    def add_actor(self):
        """
        Додає нового актора до бази даних, отримуючи інформацію від користувача.

        :return: None
        """
        name = self.display.get_input("actor_input", "enter_actor_name")
        birth_year_input = self.display.get_input("actor_input", "enter_birth_year")
        try:
            birth_year = int(birth_year_input)
        except ValueError:
            self.display.show_message("messages", "invalid_choice")
            return
        actor_id = self.execute_script('insert_actor.sql', (name, birth_year))
        self.display.show_message("messages", "actor_added_success", actor_id)

    def show_actors(self):
        """
        Уніфікований метод відображення всіх акторів.

        :return: None
        """
        rows = self.get_all_actors()
        self._show_messages_from_rows(
            rows,
            "messages",
            "actor_list",
            formatter=lambda row: f"ID: {row[0]}, Ім'я: {row[1]}"
        )

    def link_actor_to_movie(self, movie_id, actor_id):
        """
        Зв'язує актора з фільмом у базі даних.

        :param movie_id: ID фільму.
        :type movie_id: int
        :param actor_id: ID актора.
        :type actor_id: int
        :raises sqlite3.IntegrityError: Якщо актор вже пов'язаний з фільмом.
        :return: None
        """
        try:
            self.execute_script('link_actor_to_movie.sql', (movie_id, actor_id))
            self.display.show_message("messages", "actor_added_success", actor_id)
        except sqlite3.IntegrityError:
            self.display.show_message("messages", "actor_already_linked", actor_id)

    def show_movies_with_actors(self):
        """
        Показує лише ті фільми, у яких є пов'язані актори.

        :return: None
        """
        rows = self.execute_script('get_movies_with_actors.sql', fetch=True)

        if rows:
            self.display.show_messages([f"Фільм: {row[0]}, Актори: {row[1]}" for row in rows])
        else:
            self.display.show_message("messages", "no_movies_available")

    def show_movies_with_age(self):
        """
        Відображає фільми з їхнім віком.

        :return: None
        """
        rows = self.execute_script('get_movies_with_release_year.sql', fetch=True)

        if rows:
            formatted_rows = [(row[0], self.movie_age(row[1])) for row in
                              rows]  # row[0] - назва фільму, row[1] - рік випуску
            self.display.show_formatted_messages("movie_details", "movie_with_age", formatted_rows)
        else:
            self.display.show_message("messages", "no_data_available")

    def show_unique_genres(self):
        """
        Показує унікальні жанри фільмів.

        :return: None
        """
        rows = self.execute_script('get_unique_genres.sql', fetch=True)

        if rows:
            self.display.show_messages([f"Унікальний жанр: {row[0]}" for row in rows])
        else:
            self.display.show_message("messages", "no_data_available")

    def show_movie_count_by_genre(self):
        """
        Показує кількість фільмів за жанрами.

        :return: None
        """
        rows = self.execute_script('count_movies_by_genre.sql', fetch=True)

        if rows:
            self.display.show_messages([f"Жанр: {row[0]}, Кількість фільмів: {row[1]}" for row in rows])
        else:
            self.display.show_message("messages", "no_data_available")

    def show_avg_birth_year_by_genre(self):
        """
        Показує середній рік народження акторів у фільмах певного жанру.

        :return: None
        """
        genre = self.display.get_input("movie_input", "enter_genre")
        rows = self.execute_script('avg_birth_year_by_genre.sql', (genre,), fetch=True)

        if rows and rows[0][0] is not None:
            avg_birth_year = round(float(rows[0][0]), 2)  # Середній рік народження
            genre = str(genre).strip()  # Переконаємось, що жанр у строковому форматі та видаляємо зайві пробіли
            self.display.show_formatted_messages("movie_details", "avg_birth_year_by_genre",
                                                 (genre, str(avg_birth_year)))
        else:
            self.display.show_message("messages", "no_data_available")

    def _show_formatted_or_default(self, query, params, category, key, data_formatter=lambda row: row):
        """
        Уніфікований метод для виконання запиту та відображення даних з форматуванням.

        :param query: SQL-запит для виконання.
        :type query: str
        :param params: Параметри для передачі в SQL-запит.
        :type params: tuple
        :param category: Категорія повідомлення.
        :type category: str
        :param key: Ключ повідомлення.
        :type key: str
        :param data_formatter: Функція для форматування рядків результату. За замовчуванням lambda row: row.
        :type data_formatter: callable, опціонально
        :return: None
        """
        rows = self.execute_query(query, params, fetch=True)
        if rows:
            formatted_data = [data_formatter(row) for row in rows]
            self.display.show_formatted_messages(category, key, formatted_data)
        else:
            self.display.show_message("messages", "no_data_available")

    def _show_messages_from_rows(self, rows, category, key, formatter=lambda row: row):
        """
        Уніфікований метод для відображення повідомлень з форматуванням.

        :param rows: Список рядків результату запиту.
        :type rows: list
        :param category: Категорія повідомлення.
        :type category: str
        :param key: Ключ повідомлення.
        :type key: str
        :param formatter: Функція для форматування рядків. За замовчуванням lambda row: row.
        :type formatter: callable, опціонально
        :return: None
        """
        if rows:
            formatted_data = [formatter(row) for row in rows]
            self.display.show_formatted_messages(category, key, formatted_data)
        else:
            self.display.show_message("messages", "no_data_available")

    def search_movie_by_title(self):
        """
        Пошук фільмів за назвою з використанням SQL-скрипта.

        :return: None
        """
        keyword = self.display.get_input("movie_input", "enter_keyword")
        rows = self.execute_script('search_movie_by_title.sql', ('%' + keyword + '%',), fetch=True)

        if rows:
            formatted_rows = [
                (row[0] if row[0] else "Невідомо", row[1] if isinstance(row[1], int) else "Невідомий рік")
                for row in rows
            ]
            self.display.show_formatted_messages("movie_details", "movie_found", formatted_rows)
        else:
            self.display.show_message("messages", "no_movies_available")

    def show_actors_and_movies(self):
        """
        Показує імена всіх акторів та назви всіх фільмів без дублів акторів.

        :return: None
        """
        rows = self.execute_script('select_actors_and_movies.sql', fetch=True)

        if rows:
            messages = []
            for row in rows:
                actor_name = row[0]  # Имя актёра
                movie_list = row[1]  # Список фильмов (строка с фильмами, разделёнными запятыми)

                # Преобразуем строку с фильмами в список
                movies = movie_list.split(', ')

                # Проверяем, один ли фильм или несколько
                if len(movies) == 1:
                    messages.append(f"Aктор: {actor_name}, Фільм: {movies[0]}")
                else:
                    messages.append(f"Aктор: {actor_name}, Фільми: {movie_list}")

                self.display.show_messages(messages)
        else:
            self.display.show_message("messages", "no_data_available")

    def show_movies_paginated(self):
        """
        Показує фільми з пагінацією, дозволяючи користувачу переглядати сторінки.

        :return: None
        """
        page_size = 5  # Кількість фільмів на сторінці
        current_page = 1

        while True:
            offset = (current_page - 1) * page_size
            rows = self.execute_script('get_movies_paginated.sql', (page_size, offset), fetch=True)

            if not rows:
                if current_page == 1:
                    self.display.show_message("messages", "no_movies_available")
                else:
                    self.display.show_message("messages", "no_more_movies")
                break

            # Відображаємо повідомлення про поточну сторінку
            self.display.show_message("pagination", "displaying_page", current_page)

            self._show_messages_from_rows(
                rows,
                "movie_details",
                "movie_list_paginated",
                formatter=lambda row: f"ID: {row[0]}, Назва: {row[1]}, Рік випуску: {row[2]}, Жанр: {row[3]}"
            )

            # Опції навігації
            self.display.show_message("pagination", "navigation_options")
            action = self.display.get_input("pagination", "choose_option").lower()

            if action == 'n':
                current_page += 1
            elif action == 'p':
                if current_page > 1:
                    current_page -= 1
                else:
                    self.display.show_message("messages", "already_first_page")
            elif action == 'e':
                break
            else:
                self.display.show_message("messages", "invalid_option")
