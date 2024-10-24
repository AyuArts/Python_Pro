import random
import multiprocessing

class Organism:
    def __init__(self, energy, reproduction_chance, survival_chance):
        """
        Ініціалізація організму з параметрами енергії, ймовірності розмноження і виживання.
        :param energy: Початкова енергія організму.
        :param reproduction_chance: Ймовірність розмноження.
        :param survival_chance: Ймовірність виживання.
        """
        self.energy = energy
        self.reproduction_chance = reproduction_chance
        self.survival_chance = survival_chance

    def feed(self, food_amount):
        """
        Метод для збільшення енергії організму на основі кількості їжі.
        :param food_amount: Кількість отриманої їжі.
        """
        self.energy += food_amount

    def evolve(self):
        """
        Метод для еволюції організму. Визначає, чи організм розмножиться або виживе.
        :return: Новий організм або стан виживання.
        """
        if random.random() < self.reproduction_chance:
            return self.reproduce()
        if random.random() < self.survival_chance:
            return True
        return False

    def reproduce(self):
        """
        Метод для розмноження організму. Повертає новий організм.
        :return: Новий організм з подібними характеристиками.
        """
        return Organism(
            energy=self.energy // 2,
            reproduction_chance=self.reproduction_chance,
            survival_chance=self.survival_chance
        )


class Environment():
    def __init__(self, food_supply):
        """
        Ініціалізація середовища з параметром запасу їжі.
        :param food_supply: Запас їжі в середовищі.
        """
        self.food_supply = food_supply

    def provide_food(self):
        """
        Метод для надання організму певної кількості їжі.
        :return: Кількість їжі для організму.
        """
        return random.randint(0, self.food_supply)


def process_organism(organism, environment):
    """
    Функція для обробки організму. Кожен організм отримує їжу, а потім еволюціонує.
    :param organism: Об'єкт організму.
    :param environment: Об'єкт середовища.
    """
    food = environment.provide_food()
    organism.feed(food)
    evolved = organism.evolve()
    if evolved:
        print("Организм эволюционировал!")
    else:
        print("Организм не эволюционировал.")


if __name__ == "__main__":
    # Створюємо популяцію організмів
    population = [Organism(energy=100, reproduction_chance=0.5, survival_chance=0.7) for _ in range(10)]
    # Створюємо середовище з певним запасом їжі
    environment = Environment(food_supply=50)

    # Створюємо процеси для кожного організму
    processes = []
    for organism in population:
        process = multiprocessing.Process(target=process_organism, args=(organism, environment))
        processes.append(process)
        process.start()

    # Очікуємо завершення кожного процесу
    for process in processes:
        process.join()
