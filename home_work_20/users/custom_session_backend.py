from cryptography.fernet import Fernet
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import salted_hmac, constant_time_compare
from django.conf import settings
import json

class SessionStore(SessionBase):
    """
    Кастомное хранилище сессий, сохраняющее данные в cookies с подписанными значениями.
    """

    def __init__(self, session_key=None):
        super().__init__(session_key)

    def load(self):
        """
        Загружает данные сессии из cookies.
        """
        session_data = self.session_key
        if not session_data:
            return {}
        try:
            return self.decode(session_data)
        except Exception:
            return {}

    def create(self):
        """
        Создаёт новую сессию.
        """
        self._session_key = self._get_new_session_key()
        self.modified = True

    def save(self, must_create=False):
        """
        Сохраняет данные сессии в cookies.
        """
        self._session_key = self.encode(self._get_session(no_load=must_create))

    def exists(self, session_key):
        """
        Проверка существования сессии. Не актуально для хранения в cookies.
        """
        return False

    def delete(self, session_key=None):
        """
        Удаляет сессию.
        """
        self._session_key = ''
        self._session_cache = {}

    def encode(self, session_dict):
        """
        Кодирует и подписывает данные сессии.
        """
        serialized = json.dumps(session_dict)
        key_salt = "django.contrib.sessions.backends.signed_cookies"
        signature = salted_hmac(key_salt, serialized, secret=settings.SECRET_KEY).hexdigest()
        return f"{serialized}:{signature}"

    def decode(self, session_data):
        """
        Проверяет подпись и декодирует данные сессии.
        """
        key_salt = "django.contrib.sessions.backends.signed_cookies"
        try:
            serialized_data, signature = session_data.rsplit(':', 1)
            expected_signature = salted_hmac(key_salt, serialized_data, secret=settings.SECRET_KEY).hexdigest()
            if not constant_time_compare(signature, expected_signature):
                raise ValueError("Подпись некорректна.")
            return json.loads(serialized_data)
        except Exception:
            return {}
class CustomSession(SessionBase):
    """
    Кастомный бэкенд сессий с шифрованием данных.
    """

    def __init__(self, request):
        self.request = request
        self.session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        self._session_cache = None
        self.crypto = Fernet(settings.SECRET_KEY[:32].encode())

    def _get_session(self):
        if self._session_cache is not None:
            return self._session_cache
        if self.session_key:
            try:
                data = self.crypto.decrypt(self.session_key.encode()).decode()
                self._session_cache = json.loads(data)
            except Exception:
                self._session_cache = {}
        else:
            self._session_cache = {}
        return self._session_cache

    def _set_session(self, session_data):
        self._session_cache = session_data

    session = property(_get_session, _set_session)

    def create(self):
        self._session_key = self._get_new_session_key()
        self.modified = True

    def save(self, must_create=False):
        if self.session_key is None:
            self.create()
        session_data = json.dumps(self._session_cache).encode()
        encrypted_data = self.crypto.encrypt(session_data).decode()
        self.request.COOKIES[settings.SESSION_COOKIE_NAME] = encrypted_data

    def delete(self, session_key=None):
        self._session_key = None
        self._session_cache = {}
        self.modified = True
