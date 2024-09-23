# Task 7 ==============================================

total_expense = 0.0



def add_expense(amount):
    global total_expense
    total_expense += amount
    print(f"Витрата у розмірі {amount} грн додана.")



def get_expense():
    return total_expense



def main():
    while True:
        print("\nМеню:"
        "\n1. Додати витрати"
        "\n2. Переглянути загальну суму витрат"
        "\n3. Вийти")

        choice = input("Оберіть дію (1/2/3): ")

        if choice == '1':
            try:
                amount = float(input("Введіть суму витрат (грн): "))
                add_expense(amount)
            except ValueError:
                print("Будь ласка, введіть коректну числову суму.")
        elif choice == '2':
            total = get_expense()
            print(f"Загальна сума витрат: {total} грн")
        elif choice == '3':
            print("Вихід з програми.")
            break
        else:
            print("Некоректний вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main()
