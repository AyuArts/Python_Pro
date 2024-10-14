class AgeVerifier:
    """
    Клас для перевірки віку користувачів.
    """

    @staticmethod
    def is_adult(age: int) -> bool:
        """
        Повертає True, якщо вік більше або дорівнює 18, інакше False.

        :param age: Вік користувача.
        :type age: int
        :return: True якщо вік >= 18, інакше False.
        :rtype: bool
        :raises ValueError: Якщо вік є негативним числом.

        :example:
        >>> AgeVerifier.is_adult(20)
        True
        >>> AgeVerifier.is_adult(17)
        False
        """
        if age < 0:
            raise ValueError("Вік не може бути негативним.")
        return age >= 18
