import pytest
from age_verifier import AgeVerifier

@pytest.mark.parametrize("age, expected", [
    (17, False),
    (18, True),
    (30, True),
    (0, False),
    (120, True),
])
def test_is_adult_valid_ages(age, expected):
    """
    Перевіряє правильну роботу функції для різних коректних значень віку.

    :param age: Вік для тестування.
    :type age: int
    :param expected: Очікуваний результат.
    :type expected: bool
    """
    assert AgeVerifier.is_adult(age) == expected

@pytest.mark.parametrize("age", [-1, -20, -100])
def test_is_adult_negative_age(age):
    """
    Перевіряє, чи піднімається виняток ValueError для негативних значень віку.

    :param age: Некоректний вік для тестування.
    :type age: int
    """
    with pytest.raises(ValueError):
        AgeVerifier.is_adult(age)

@pytest.mark.parametrize("age", [121, 130, 150])
def test_is_adult_unlikely_age(age):
    """
    Використовує умовний скіп для пропуску тестів з малоймовірними значеннями віку (>120).

    :param age: Некоректний вік для тестування.
    :type age: int
    """
    if age > 120:
        pytest.skip(f"Пропущено тестування для віку {age}, оскільки це малоймовірний сценарій.")
    assert AgeVerifier.is_adult(age) == False

def test_is_adult_skip_if_age_unlikely():
    """
    Альтернативний спосіб використання умовного пропуску з pytest.skip.
    """
    age = 121
    if age > 120:
        pytest.skip("Неправильне значення віку")
    assert AgeVerifier.is_adult(age) == False
