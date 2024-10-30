from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pandas as pd
import csv


class NewsScraper:
    def __init__(self, url, days=7):
        """
        Ініціалізація класу для парсингу новин.

        :param url: URL сторінки для парсингу новин.
        :param days: Кількість днів для фільтрації новин.
        """
        self.url = url
        self.days = days
        self.driver = webdriver.Chrome()
        self.all_news = []
        self.seven_days_ago = datetime.today() - timedelta(days=self.days)

    def load_page(self):
        """
        Завантажує сторінку новин у Selenium WebDriver.
        """
        self.driver.get(self.url)
        time.sleep(7)

    def scroll_page(self, scroll_pause_time=0.8, scroll_step=300):
        """
        Прокручує сторінку, щоб підвантажити нові новини.

        :param scroll_pause_time: Пауза між прокрутками.
        :param scroll_step: Крок прокрутки в пікселях.
        """
        last_height = self.get_page_height()
        stop_scrolling = False
        while not stop_scrolling:
            self.smooth_scroll(scroll_step, scroll_pause_time)
            time.sleep(3)
            stop_scrolling = self.parse_and_append_news()
            new_height = self.get_page_height()
            if new_height == last_height:
                break
            last_height = new_height

    def smooth_scroll(self, scroll_step, scroll_pause_time):
        """
        Плавно прокручує сторінку невеликими кроками.

        :param scroll_step: Крок прокрутки в пікселях.
        :param scroll_pause_time: Пауза між скролами.
        """
        for _ in range(0, self.get_page_height(), scroll_step):
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(scroll_pause_time)

    def get_page_height(self):
        """
        Повертає поточну висоту сторінки.

        :return: Висота сторінки.
        """
        return self.driver.execute_script("return document.body.scrollHeight")

    def parse_and_append_news(self):
        """
        Парсить сторінку, витягуючи новини, і додає їх до списку.

        :return: Булеве значення, що вказує, чи потрібно зупинити прокрутку.
        """
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        news, stop_scrolling = self.extract_news(soup, self.seven_days_ago)
        self.all_news.extend(news)
        return stop_scrolling

    def extract_news(self, soup, seven_days_ago):
        """
        Витягує новини з HTML-коду сторінки.

        :param soup: BeautifulSoup об'єкт з HTML-кодом сторінки.
        :param seven_days_ago: Дата для фільтрації новин.
        :return: Кортеж зі списку новин та булевого значення для зупинки.
        """
        news = []
        articles = soup.find_all("article", class_="post")

        for article in articles:
            news_data = self.extract_news_data(article)
            if not news_data:
                continue
            news_date = news_data['date']
            if news_date < seven_days_ago:
                return news, True
            news.append(news_data)
        return news, False

    def extract_news_data(self, article):
        """
        Витягує дані однієї новини (заголовок, посилання, дату та опис).

        :param article: HTML елемент новини.
        :return: Словник з даними новини або None, якщо формат даних невірний.
        """
        date_tag = article.find("div", class_="cs-meta-date")
        if not date_tag:
            return None
        try:
            news_date = datetime.strptime(date_tag.get_text(strip=True), "%d.%m.%y")
        except ValueError:
            return None  # Пропустити новину, якщо формат дати невірний

        title = article.find("p").get_text(strip=True) if article.find("p") else "Без назви"
        link_tag = article.find("a", href=True)
        link = link_tag['href'] if link_tag else "Немає посилання"
        summary = article.find("div", class_="summary").get_text(strip=True) if article.find("div",
                                                                                             class_="summary") else "Немає опису"

        return {
            "title": title,
            "link": link,
            "date": news_date,
            "summary": summary
        }

    def save_to_csv(self, filename="news.csv"):
        """
        Зберігає зібрані новини у файл CSV.

        :param filename: Назва файлу CSV.
        """
        df = pd.DataFrame(self.all_news)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Новини збережено у файл {filename}")

    def generate_report(self):
        """
        Генерує звіт про кількість новин за кожний день.
        """
        df = pd.DataFrame(self.all_news)
        report = df.groupby(df['date'].dt.date).size()
        print("Кількість новин за кожний день:")
        print(report)

    def close(self):
        """
        Закриває Selenium WebDriver.
        """
        self.driver.quit()

    def run(self):
        """
        Запускає процес парсингу, включаючи завантаження сторінки, прокрутку, збір даних та збереження.
        """
        try:
            self.load_page()
            self.scroll_page()
            self.save_to_csv()
            self.generate_report()
        finally:
            self.close()


if __name__ == "__main__":
    url = "https://nakypilo.ua/novyny/?gad_source=1&gclid=Cj0KCQjwsoe5BhDiARIsAOXVoUuWxyALJ7vLfzu7ngxbDi72tQGgoAP0Z8p6KOW4_VuAGDx23L8dU94aAmBUEALw_wcB"
    scraper = NewsScraper(url)
    scraper.run()
