from django.shortcuts import render
from django.views import View
from django.utils import timezone

# Функціональні відображення

def home(request):
    """
    Відображає головну сторінку веб-сайту.

    :param request: HTTP-запит.
    :return: Відповідь з рендерингом шаблону 'main/home.html'.
    """
    return render(request, 'main/home.html')

def about(request):
    """
    Відображає сторінку "Про нас" з інформацією про компанію.

    :param request: HTTP-запит.
    :return: Відповідь з рендерингом шаблону 'main/about.html', де передаються:
             - 'company_history': Історія компанії.
             - 'mission': Місія компанії (None, якщо інформація відсутня).
             - 'updated_date': Дата оновлення сторінки.
    """
    return render(request, 'main/about.html', {
        'company_history': 'Наша компанія була заснована в 2020 році...',
        'mission': None,
        'updated_date': timezone.now()
    })

# Класові відображення

class ContactView(View):
    """
    Відображає контактну сторінку з інформацією про контактні дані компанії.
    """

    def get(self, request):
        """
        Обробляє GET-запит для сторінки контактів.

        :param request: HTTP-запит.
        :return: Відповідь з рендерингом шаблону 'main/contact.html', де передаються:
                 - 'address': Адреса компанії.
                 - 'phone': Телефон компанії.
                 - 'email': Електронна пошта компанії.
        """
        contact_info = {
            'address': '1234 Main St, Kyiv',
            'phone': '+380 123 456 789',
            'email': 'contact@company.com'
        }
        return render(request, 'main/contact.html', contact_info)

class ServiceView(View):
    """
    Відображає сторінку "Послуги" з переліком послуг компанії.
    """

    def get(self, request):
        """
        Обробляє GET-запит для сторінки послуг.

        :param request: HTTP-запит.
        :return: Відповідь з рендерингом шаблону 'main/services.html', де передаються:
                 - 'services': Список послуг компанії, де кожна послуга містить:
                   - 'name': Назва послуги.
                   - 'description': Опис послуги.
        """
        services = [
            {'name': 'Консультація', 'description': 'Професійні консультації'},
            {'name': 'Аудит', 'description': 'Детальний аналіз процесів'},
            {'name': 'Розробка', 'description': 'Індивідуальні рішення для вашого бізнесу'}
        ]
        return render(request, 'main/services.html', {'services': services})
