import pytest
from bank_account import BankAccount


@pytest.fixture
def bank_account(mocker) -> BankAccount:
    """
    Фікстура для створення екземпляра BankAccount з початковим балансом 200 та змокованим методом get_balance.

    :return: Екземпляр BankAccount з початковим балансом.
    :rtype: BankAccount
    """
    account = BankAccount(200)  # Встановлюємо початковий баланс на 200

    mocker.patch.object(account, 'get_balance', return_value=account.balance)
    return account


@pytest.mark.parametrize(
    "deposit_amount, expected_message",
    [
        (200, "Ваш баланс поповнено на суму: 200."),
        (0, "Сума повинна бути більшою за 0.")
    ],
    ids=["Valid deposit", "Deposit zero"]
)
def test_deposit(bank_account, deposit_amount, expected_message):
    assert bank_account.deposit(deposit_amount) == expected_message


@pytest.mark.parametrize(
    "withdraw_amount, expected_message",
    [
        (200, "З вашого рахунку списана сума: 200.\nВаш баланс становить: 0."),
        (300, "На вашому рахунку недостатньо коштів."),
        (0, "Сума для зняття повинна бути більшою за 0.")
    ],
    ids=["Successful withdrawal", "Not enough funds", "Amount less than or equal to 0"]
)
def test_withdraw(bank_account, withdraw_amount, expected_message):
    if bank_account.balance == 0:
        pytest.skip("Пропуск тесту зняття коштів, оскільки баланс рахунку дорівнює нулю.")
    assert bank_account.withdraw(withdraw_amount) == expected_message


def test_get_balance(mocker):
    account = BankAccount(0)
    account.account_id = 123

    fake_response = {
        'balance': 500
    }

    # Мокаємо метод requests.get
    mock_get = mocker.patch('bank_account.requests.get')

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_response

    balance = account.get_balance()
    assert balance == 500
    assert account.balance == 500

    # Перевіряємо, що запит був зроблений з правильними параметрами
    mock_get.assert_called_with("https://api.bank.com/balance", params={"account_id": 123})
