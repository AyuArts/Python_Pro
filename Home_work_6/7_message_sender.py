class MessageSender:
    """
    Інтерфейс для відправки повідомлень через різні канали.

    Методи:
        send_message(message: str): Відправка повідомлення.
    """

    def send_message(self, message: str):
        """
        Абстрактний метод для відправки повідомлення.

        Аргументи:
            message (str): Текст повідомлення для відправки.
        """
        pass


class SMSService:
    """
    Клас для відправки повідомлень через SMS.

    Методи:
        send_sms(phone_number: str, message: str): Відправка SMS.
    """

    def send_sms(self, phone_number, message):
        """
        Відправка SMS повідомлення на зазначений номер.

        Аргументи:
            phone_number (str): Номер телефону отримувача.
            message (str): Текст повідомлення.

        Викидає:
            Exception: У разі, якщо відправка не вдалася.
        """
        print(f"Відправка SMS на {phone_number}: {message}")
        if phone_number == "error":
            raise Exception("Не вдалося відправити SMS")


class EmailService:
    """
    Клас для відправки повідомлень через Email.

    Методи:
        send_email(email_address: str, message: str): Відправка Email.
    """

    def send_email(self, email_address, message):
        """
        Відправка Email повідомлення на зазначену адресу.

        Аргументи:
            email_address (str): Адреса електронної пошти отримувача.
            message (str): Текст повідомлення.

        Викидає:
            Exception: У разі, якщо відправка не вдалася.
        """
        print(f"Відправка Email на {email_address}: {message}")
        if email_address == "error@example.com":
            raise Exception("Не вдалося відправити Email")


class PushService:
    """
    Клас для відправки Push-повідомлень.

    Методи:
        send_push(device_id: str, message: str): Відправка Push-повідомлення.
    """

    def send_push(self, device_id, message):
        """
        Відправка Push-повідомлення на зазначений пристрій.

        Аргументи:
            device_id (str): Ідентифікатор пристрою отримувача.
            message (str): Текст повідомлення.

        Викидає:
            Exception: У разі, якщо відправка не вдалася.
        """
        print(f"Відправка Push-повідомлення на пристрій {device_id}: {message}")
        if device_id == "error_device":
            raise Exception("Не вдалося відправити Push-повідомлення")


class SMSAdapter(MessageSender):
    """
    Адаптер для використання SMSService через інтерфейс MessageSender.

    Атрибути:
        sms_service (SMSService): Сервіс для відправки SMS.
        phone_number (str): Номер телефону отримувача.
    """

    def __init__(self, sms_service, phone_number):
        """
        Ініціалізує адаптер для SMSService.

        Аргументи:
            sms_service (SMSService): Сервіс для відправки SMS.
            phone_number (str): Номер телефону отримувача.
        """
        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str):
        """
        Відправляє повідомлення через SMSService.

        Аргументи:
            message (str): Текст повідомлення для відправки.
        """
        try:
            self.sms_service.send_sms(self.phone_number, message)
        except Exception as e:
            print(f"Помилка при відправці SMS: {e}")


class EmailAdapter(MessageSender):
    """
    Адаптер для використання EmailService через інтерфейс MessageSender.

    Атрибути:
        email_service (EmailService): Сервіс для відправки Email.
        email_address (str): Адреса електронної пошти отримувача.
    """

    def __init__(self, email_service, email_address):
        """
        Ініціалізує адаптер для EmailService.

        Аргументи:
            email_service (EmailService): Сервіс для відправки Email.
            email_address (str): Адреса електронної пошти отримувача.
        """
        self.email_service = email_service
        self.email_address = email_address

    def send_message(self, message: str):
        """
        Відправляє повідомлення через EmailService.

        Аргументи:
            message (str): Текст повідомлення для відправки.
        """
        try:
            self.email_service.send_email(self.email_address, message)
        except Exception as e:
            print(f"Помилка при відправці Email: {e}")


class PushAdapter(MessageSender):
    """
    Адаптер для використання PushService через інтерфейс MessageSender.

    Атрибути:
        push_service (PushService): Сервіс для відправки Push-повідомлень.
        device_id (str): Ідентифікатор пристрою отримувача.
    """

    def __init__(self, push_service, device_id):
        """
        Ініціалізує адаптер для PushService.

        Аргументи:
            push_service (PushService): Сервіс для відправки Push-повідомлень.
            device_id (str): Ідентифікатор пристрою отримувача.
        """
        self.push_service = push_service
        self.device_id = device_id

    def send_message(self, message: str):
        """
        Відправляє повідомлення через PushService.

        Аргументи:
            message (str): Текст повідомлення для відправки.
        """
        try:
            self.push_service.send_push(self.device_id, message)
        except Exception as e:
            print(f"Помилка при відправці Push-повідомлення: {e}")


def send_message_to_all(adapters, message):
    """
    Відправляє повідомлення через всі сервіси.

    Аргументи:
        adapters (list): Список адаптерів для відправки повідомлень.
        message (str): Текст повідомлення для відправки.
    """
    for adapter in adapters:
        adapter.send_message(message)


# Використання
sms_service = SMSService()
email_service = EmailService()
push_service = PushService()

sms_adapter = SMSAdapter(sms_service, "+380123456789")
email_adapter = EmailAdapter(email_service, "user@example.com")
push_adapter = PushAdapter(push_service, "device123")

adapters = [sms_adapter, email_adapter, push_adapter]

message = "Привіт! Це тестове повідомлення."

# Відправка повідомлення через усі сервіси
send_message_to_all(adapters, message)
