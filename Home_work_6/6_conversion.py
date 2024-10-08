import json
import csv
from lxml import etree as ET
import os
import re

# Завантажуємо конфігурацію з файлу
with open('config.json', 'r', encoding='utf-8') as config_file:
    conf = json.load(config_file)

class Conversion:
    """
    Клас для роботи з файлами форматів CSV, JSON та XML. Дозволяє читати, відображати
    та конвертувати файли між різними форматами.
    """

    def __init__(self, file):
        """
        Ініціалізує об'єкт класу Conversion.

        :param file: Назва файлу для обробки.
        """
        self.file = file
        self.file_extension = os.path.splitext(self.file)[1].lower()
        self.file_conf = self.get_file_conf()
        self.file_type = self.file_conf['type']

    def get_file_conf(self):
        """
        Отримує конфігурацію для даного розширення файлу.

        :return: Конфігурація для файлу.
        :raises ValueError: Якщо формат файлу не підтримується.
        """
        if self.file_extension in conf['file_types']:
            return conf['file_types'][self.file_extension]
        else:
            raise ValueError("Непідтримуваний формат файлу. Підтримуються лише CSV, JSON та XML.")

    def read_file(self):
        """
        Універсальний метод для читання файлів різних типів.

        :return: Дані, прочитані з файлу (список або словник).
        """
        mode = self.file_conf['mode']
        open_kwargs = self.file_conf['kwargs']

        with open(self.file, mode, **open_kwargs) as f:
            parser_method_name = self.file_conf['parser']
            parse_function = getattr(self, parser_method_name)
            return parse_function(f)

    def parse_csv(self, file_obj):
        """
        Парсить CSV-файл та повертає список словників.

        :param file_obj: Об'єкт файлу для читання.
        :return: Список словників з даними CSV.
        """
        reader = csv.DictReader(file_obj)
        return list(reader)

    def parse_json(self, file_obj):
        """
        Парсить JSON-файл та повертає дані.

        :param file_obj: Об'єкт файлу для читання.
        :return: Дані з JSON у вигляді словника або списку.
        """
        return json.load(file_obj)

    def parse_xml(self, file_obj):
        """
        Парсить XML-файл та повертає список словників з даними.

        :param file_obj: Об'єкт файлу для читання.
        :return: Список словників, де кожен елемент є записом з XML.
        """
        content = file_obj.read()
        root = ET.fromstring(content)
        result = []
        for element in root:
            item = {}
            for child in element:
                item[child.tag] = child.text
            result.append(item)
        return result

    def display_file(self):
        """
        Виводить дані файлу на екран у універсальному форматі.

        :return: None
        """
        data = self.read_file()

        print(self.file_conf['message'])

        if not isinstance(data, list):
            data = [data]

        for item in data:
            print(item)

    def make_valid_xml_tag(self, tag):
        """
        Робить назву тегу валідною для XML, видаляючи недопустимі символи.

        :param tag: Початкова назва тегу.
        :return: Валідна назва тегу.
        """
        # Видаляємо недопустимі символи
        tag = re.sub(r'[^\w\-\.]', '', tag, flags=re.UNICODE)
        # Якщо тег починається не з літери або '_', додаємо '_'
        if not re.match(r'^[\w]', tag, flags=re.UNICODE):
            tag = '_' + tag
        return tag

    def write_file(self, data, output_format, output_file):
        """
        Універсальний метод для запису даних у файл вказаного формату.

        :param data: Дані для запису.
        :param output_format: Формат для запису (csv, json, xml).
        :param output_file: Ім'я вихідного файлу для запису.
        :return: None
        :raises ValueError: Якщо вказаний формат не підтримується.
        """
        if output_format not in conf['available_formats']:
            raise ValueError(f"Непідтримуваний формат для запису: {output_format}")

        target_conf = None
        for ext, settings in conf['file_types'].items():
            if settings['type'] == output_format:
                target_conf = settings
                break
        else:
            raise ValueError(f"Конфігурація для формату {output_format} не знайдена.")

        write_mode = target_conf['write_mode']
        write_kwargs = target_conf.get('kwargs', {})
        writer_method_name = target_conf['writer']

        with open(output_file, mode=write_mode, **write_kwargs) as f:
            write_function = getattr(self, writer_method_name)
            write_function(data, f)

    def write_csv(self, data, file_obj):
        """
        Записує дані у CSV файл.

        :param data: Дані для запису у файл.
        :param file_obj: Об'єкт файлу для запису.
        :return: None
        """
        if not data:
            raise ValueError("Немає даних для запису.")

        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = list(fieldnames)

        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    def write_json(self, data, file_obj):
        """
        Записує дані у JSON файл.

        :param data: Дані для запису у файл.
        :param file_obj: Об'єкт файлу для запису.
        :return: None
        """
        json.dump(data, file_obj, indent=4, ensure_ascii=False)

    def write_xml(self, data, file_obj):
        """
        Записує дані у XML файл.

        :param data: Дані для запису у файл.
        :param file_obj: Об'єкт файлу для запису.
        :return: None
        """
        root = ET.Element("root")

        for item in data:
            element = ET.Element("item")
            for key, value in item.items():
                valid_key = self.make_valid_xml_tag(key)
                child = ET.SubElement(element, valid_key)
                child.text = str(value)
            root.append(element)

        tree = ET.ElementTree(root)
        tree.write(file_obj, encoding='utf-8', xml_declaration=True)

    def convert_to(self, output_format):
        """
        Конвертує дані у вказаний формат та зберігає їх у файл.

        :param output_format: Формат для конвертації (csv, json, xml).
        :return: None
        """
        data = self.read_file()

        base_name = os.path.splitext(self.file)[0]
        output_file = f"{base_name}_converted.{output_format}"

        self.write_file(data, output_format, output_file)
        print(f"Файл успішно конвертовано та збережено як {output_file}")

def main_menu():
    """
    Головне меню програми для вибору файлу та конвертації.

    :return: None
    """
    file_name = input("Введіть ім'я файлу для обробки: ")
    if not os.path.isfile(file_name):
        print("Файл не знайдено. Будь ласка, перевірте ім'я файлу і спробуйте знову.")
        return

    try:
        conversion = Conversion(file_name)
        conversion.display_file()

        # Доступні формати для конвертації
        available_formats = conf['available_formats'].copy()
        # Видаляємо поточний формат файлу з доступних для конвертації
        available_formats.remove(conversion.file_type)

        if available_formats:
            print("\nОберіть формат для конвертації:")
            for idx, fmt in enumerate(available_formats, start=1):
                print(f"{idx}. {fmt.upper()}")

            choice = input("Введіть номер обраного формату або натисніть Enter для пропуску: ")

            if choice:
                try:
                    choice = int(choice)
                    if 1 <= choice <= len(available_formats):
                        output_format = available_formats[choice - 1]
                        conversion.convert_to(output_format)
                    else:
                        print("Некоректний вибір. Конвертація скасована.")
                except ValueError:
                    print("Некоректне введення. Конвертація скасована.")
            else:
                print("Конвертація пропущена.")
        else:
            print("Немає доступних форматів для конвертації.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main_menu()
