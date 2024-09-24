# Task 4

def training_session(number_of_rounds):
    """
    Проводить тренувальну сесію з кількома раундами.

    Аргументи:
    number_of_rounds (int): Кількість раундів тренування.
    """
    time_per_round = default_time
    count_rounds = number_of_rounds
    number_round = 1

    def adjust_time():
        """Коригує час для кожного раунду."""
        nonlocal time_per_round
        time_per_round -= 5

    print(f"Результат: \nРаунд {number_round}: {time_per_round} хвилин")

    while count_rounds != 1 and time_per_round != 0:
        count_rounds -= 1
        adjust_time()
        number_round += 1
        print(f"Раунд {number_round}: {time_per_round} хвилин (після коригування часу)")


default_time = 60
training_session(3)
