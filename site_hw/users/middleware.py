from datetime import timedelta
from django.utils.timezone import now


class RefreshCookieMiddleware:
    """
    Middleware для оновлення терміну дії cookies, якщо користувач активно використовує програму.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Перевіряємо, чи є "username" у cookies
        if 'username' in request.COOKIES:
            # Оновлюємо термін дії cookies
            max_age = 3600  # Наприклад, 1 година

            response.set_cookie(
                'username',
                request.COOKIES['username'],
                max_age=max_age,  # Використовуємо лише max_age
                httponly=True,
            )

        return response
