def line_filter(file_path: str, keyword: str):
    """
    Генератор для читання великого файлу та фільтрації рядків за ключовим словом.

    :param file_path: Шлях до текстового файлу.
    :type file_path: str
    :param keyword: Ключове слово для фільтрації рядків.
    :type keyword: str
    :yield: Рядки, що містять ключове слово.
    :rtype: iterator
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if keyword in line:
                yield line

def save_filtered_lines(input_file: str, output_file: str, keyword: str):
    """
    Зберігає відфільтровані рядки з одного файлу до іншого.

    :param input_file: Шлях до вихідного файлу.
    :type input_file: str
    :param output_file: Шлях до файлу, куди записуються відфільтровані рядки.
    :type output_file: str
    :param keyword: Ключове слово для фільтрації рядків.
    :type keyword: str
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        for line in line_filter(input_file, keyword):
            output.write(line)

# Використання генератора для фільтрації рядків з ключовим словом і збереження у новий файл
input_file_path = 'test_file.log'
output_file_path = 'filtered_log_file.txt'
search_keyword = 'INFO'  # Ключове слово для пошуку

save_filtered_lines(input_file_path, output_file_path, search_keyword)
