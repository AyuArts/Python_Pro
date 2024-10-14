import requests

class BankAccount:
    def __init__(self, balance: float):
        """
        Ініціалізація банківського рахунку з вказаним балансом.

        :param balance: Початковий баланс рахунку.
        """
        self.balance = balance
        self.account_id = None

    def deposit(self, amount: float) -> str:
        """
        Поповнення рахунку на вказану суму.

        :param amount: Сума для поповнення.
        :return: Повідомлення про результат операції.
        """
        if amount <= 0:
            return "Сума повинна бути більшою за 0."
        else:
            self.balance += amount
            return f"Ваш баланс поповнено на суму: {amount}."

    def withdraw(self, amount: float) -> str:
        """
        Зняття вказаної суми з рахунку.

        :param amount: Сума для зняття.
        :return: Повідомлення про результат операції.
        """
        if amount <= 0:
            return "Сума для зняття повинна бути більшою за 0."
        elif self.balance >= amount:
            self.balance -= amount
            return f"З вашого рахунку списана сума: {amount}.\nВаш баланс становить: {self.balance}."
        else:
            return "На вашому рахунку недостатньо коштів."

    def get_balance(self) -> float:
        """
        Отримує баланс з зовнішнього API.
        :return: Поточний баланс рахунку.
        """
        response = requests.get("https://api.bank.com/balance", params={"account_id": self.account_id})
        if response.status_code == 200:
            data = response.json()
            self.balance = data['balance']
            return self.balance
        else:
            raise Exception("Не вдалося отримати баланс з API.")
