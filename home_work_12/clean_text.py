import re


def clean_text(text):
    """
    Очищує HTML-текст, видаляючи теги, зайві пробіли та рядки.

    :param text: Вхідний текст у форматі HTML.
    :type text: str
    :return: Очищений текст без HTML-тегів та зайвих пробілів.
    :rtype: str
    """
    return re.sub(r'[ \t]+', ' ',
                  re.sub(r'\s*\n\s*', '\n',
                         re.sub(r'<.*?>', '', text))).strip()


text = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Контакти</title>
</head>
<body>
    <header>
        <h1>Ласкаво просимо на наш сайт</h1>
    </header>
    <main>
        <p>Якщо у вас виникли питання, ви можете зателефонувати нам за номером <strong>(123) 456-7890</strong> або написати на електронну пошту за адресою <a href="mailto:support@example.com">support@example.com</a>.</p>

        <section>
            <h2>Контакти для зв'язку</h2>
            <ul>
                <li>Телефон: <span>123-456-7890</span></li>
                <li>Email: <a href="mailto:info@example.com">info@example.com</a></li>
                <li>Адреса: <address>вул. Тестова, 12, Київ, Україна</address></li>
            </ul>
        </section>

        <section>
            <h2>Робочі години</h2>
            <table>
                <tr>
                    <th>День</th>
                    <th>Години</th>
                </tr>
                <tr>
                    <td>Понеділок-П'ятниця</td>
                    <td>9:00 - 18:00</td>
                </tr>
                <tr>
                    <td>Субота</td>
                    <td>10:00 - 16:00</td>
                </tr>
                <tr>
                    <td>Неділя</td>
                    <td>Вихідний</td>
                </tr>
            </table>
        </section>
    </main>
    <footer>
        <p>&copy; 2024 ТОВ "Приклад". Всі права захищені.</p>
    </footer>
</body>
</html>

"""

print(clean_text(text))
