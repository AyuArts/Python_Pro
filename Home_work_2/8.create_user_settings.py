# Task 8 ==============================================

def create_user_settings():

    settings = {
        'theme': 'light',
        'language': 'English',
        'notifications': True
    }


    def settings_manager(action, key=None, value=None):
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


print(user_settings('get', 'theme'))


print(user_settings('set', 'theme', 'dark'))


print(user_settings('get', 'theme'))


print(user_settings('all'))

