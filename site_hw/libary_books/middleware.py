from django.utils.cache import patch_cache_control
from django.core.cache import cache
from django.http import HttpResponse
import hashlib

NO_CACHE_PATHS = [
    '/login/',
    '/register/',
]

class AnonymousUserCacheMiddleware:
    """
    Middleware для кеширования страниц для анонимных пользователей.
    """

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        if request.path in NO_CACHE_PATHS:
            return self.get_response(request)

        if request.method != 'GET':
            return self.get_response(request)

        cache_key = f"anon_cache_{hashlib.md5(request.get_full_path().encode()).hexdigest()}"
        response = cache.get(cache_key)
        if response:
            return response

        response = self.get_response(request)
        cache.set(cache_key, response, 900)
        patch_cache_control(response, public=True)
        return response
