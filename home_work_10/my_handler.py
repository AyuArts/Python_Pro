"""
Модуль для створення багатопотокового веб-сервера.

Цей модуль реалізує простий багатопотоковий веб-сервер, який може обслуговувати кілька
клієнтів одночасно, використовуючи потоки. Сервер відповідає на HTTP-запити клієнтів
і надсилає їм текстові повідомлення.

Класи:
    - MyHandler: Обробник запитів, який відповідає на запити HTTP-методом GET.
    - ThreadedHTTPServer: Багатопотоковий сервер, який обслуговує кожного клієнта в окремому потоці.

Функції:
    - run_server: Функція для запуску веб-сервера.
"""

import http.server
import socketserver


class MyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Клас для обробки HTTP-запитів.

    Обробляє GET-запити і надсилає відповідь з текстовим повідомленням.

    Методи:
        - do_GET: Відповідає на HTTP-запити методом GET.
    """

    def do_GET(self):
        """
        Обробляє HTTP GET-запит.

        Відправляє клієнту відповідь з кодом 200 (OK) та текстове повідомлення.

        :return: Нічого не повертає.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, this is a multi-threaded web server!")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """
    Клас багатопотокового HTTP-сервера.

    Кожен новий клієнт обробляється в окремому потоці, що дозволяє обслуговувати
    кілька клієнтів одночасно.
    """
    pass


def run_server(port=8000):
    """
    Запускає багатопотоковий веб-сервер.

    Створює екземпляр ThreadedHTTPServer і запускає сервер для обслуговування HTTP-запитів на вказаному порту.

    :param port: Номер порту для запуску сервера (за замовчуванням 8000).
    :type port: int
    :return: Нічого не повертає.
    """
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, MyHandler)

    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server(8000)
