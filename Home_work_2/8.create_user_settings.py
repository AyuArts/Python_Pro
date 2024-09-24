# Task 8

def create_user_settings():
    """
    Створює налаштування користувача і повертає функцію для їх управління.

    Повертає:
    function: Функція для управління налаштуваннями користувача.
    """
    settings = {
        'theme': 'light',
        'language': 'English',
        'notifications': True
    }

    def settings_manager(action, key=None, value=None):
        """
        Керує налаштуваннями користувача: отримує, встановлює або повертає всі налаштування.

        Аргументи:
        action (str): Дія, яку потрібно виконати ('get', 'set', 'all').
        key (str, optional): Ключ налаштування (обов'язковий для дій 'get' і 'set').
        value (optional): Значення, яке потрібно встановити для ключа (для дії 'set').

        Повертає:
        str або dict: Повертає відповідне повідомлення або всі налаштування.
        """
        nonlocal settings
        if action == 'get':
            return settings.get(key, 'Налаштування не знайдено')
        elif action == 'set':
            if key in settings:
                settings[key] = value
                return f'{key} оновлено на {value}'
            else:
                return 'Налаштування не знайдено'
        elif action == 'all':
            return settings
        else:
            return 'Невідома дія'

    return settings_manager


user_settings = create_user_settings()

# Отримання значення теми
print(user_settings('get', 'theme'))

# Оновлення значення теми на 'dark'
print(user_settings('set', 'theme', 'dark'))

# Перевірка нового значення теми
print(user_settings('get', 'theme'))

# Виведення всіх налаштувань
print(user_settings('all'))
