import requests
import unittest
from unittest.mock import patch, Mock


class WebService:
    """
    Класс WebService предоставляет метод для получения данных по HTTP-запросу.
    """

    def get_data(self, url: str) -> dict:
        """
        Выполняет HTTP GET-запрос по указанному URL и возвращает данные в формате JSON.

        Args:
            url (str): URL для отправки GET-запроса.

        Returns:
            dict: Ответ в формате JSON, если запрос выполнен успешно.

        Raises:
            requests.exceptions.HTTPError: Если запрос завершился с ошибкой.
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


class TestWebService(unittest.TestCase):
    """
    Класс для тестирования методов WebService с использованием unittest и mock.
    """

    @patch('requests.get')
    def test_get_data_success(self, mock_get):
        """
        Тестирует успешное выполнение метода get_data с мокированием requests.get.

        Мок настроен на успешный ответ (статус 200), и проверяется, что
        метод возвращает ожидаемые данные.

        Args:
            mock_get (Mock): Мок объекта requests.get.
        """
        # Настраиваем мок для успешного запроса (статус 200)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        ws = WebService()
        result = ws.get_data("http://example.com")
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("http://example.com")

    @patch('requests.get')
    def test_get_data_error(self, mock_get):
        """
        Тестирует выполнение метода get_data при ошибке запроса (например, статус 404).

        Мок настроен на ошибку HTTP-запроса, и проверяется, что
        метод выбрасывает исключение HTTPError.

        Args:
            mock_get (Mock): Мок объекта requests.get.
        """
        # Настраиваем мок для ошибки запроса (статус 404)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        ws = WebService()
        with self.assertRaises(requests.exceptions.HTTPError):
            ws.get_data("http://example.com")

        mock_get.assert_called_once_with("http://example.com")


if __name__ == '__main__':
    unittest.main()
