import logging
from django.shortcuts import render

logger = logging.getLogger('users')

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        logger.info(f'User {user} accessed {request.path}')
        response = self.get_response(request)
        return response


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code == 404:
                return render(request, 'errors/404.html', status=404)
            return response
        except Exception:
            return render(request, 'errors/500.html', status=500)
