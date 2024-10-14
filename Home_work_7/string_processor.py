import unittest


class StringProcessor:
    """
    Клас для обробки рядків, надає методи для реверсування, капіталізації,
    підрахунку голосних та приголосних букв у рядку.
    """

    def __init__(self, string):
        """
        Ініціалізує об'єкт StringProcessor з заданим рядком.

        :param string: Рядок для обробки.
        """
        self.string = string

    def reverse_string(self) -> str:
        """
        Повертає реверсований рядок.

        :return: Реверсований рядок.
        """
        return self.string[::-1]

    def capitalize_string(self) -> str:
        """
        Повертає рядок з першою заглавною літерою.

        :return: Капіталізований рядок.
        """
        return self.string.capitalize()

    def count_vowels(self) -> int:
        """
        Підраховує кількість голосних букв у рядку.

        :return: Кількість голосних букв.
        """
        vowels = 'аеиіоуєїюяАЕИІОУЄЇЮЯ'
        return sum(1 for char in self.string if char in vowels)

    def count_consonants(self) -> int:
        """
        Підраховує кількість приголосних букв у рядку.

        :return: Кількість приголосних букв.
        """
        consonants = 'бвгґджзйклмнпрстфхцчшщБВГҐДЖЗЙКЛМНПРСТФХЦЧШЩ'
        return sum(1 for char in self.string if char in consonants)


class TestStringProcessor(unittest.TestCase):
    """
    Клас для тестування методів класу StringProcessor.
    """

    def setUp(self):
        """
        Ініціалізує об'єкт StringProcessor з тестовим рядком.
        """
        # Встановлюємо атрибут з тестовим рядком
        self.processor = StringProcessor("весілля у мене сьогодні")

    @unittest.skip
    def test_reverse_string(self):
        """
        Тестує метод reverse_string.
        """
        right_decision = "індогоьс енем у весілля"
        check_it_out = self.processor.reverse_string()
        self.assertEqual(right_decision, check_it_out)

    def test_capitalize_string(self):
        """
        Тестує метод capitalize_string.
        """
        right_decision = "Весілля у мене сьогодні"
        check_it_out = self.processor.capitalize_string()
        self.assertEqual(right_decision, check_it_out)

    def test_count_vowels(self):
        """
        Тестує метод count_vowels.
        """
        right_decision = 9
        check_it_out = self.processor.count_vowels()
        self.assertEqual(right_decision, check_it_out)

    def test_count_consonants(self):
        """
        Тестує метод count_consonants.
        """
        right_decision = 10
        check_it_out = self.processor.count_consonants()
        self.assertEqual(right_decision, check_it_out)


if __name__ == '__main__':
    unittest.main()
