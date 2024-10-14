import pytest
from file_processor import FileProcessor

def test_file_write_read(tmpdir):
    """
    Тестує базову функціональність запису та читання файлу.

    :param tmpdir: Фікстура pytest для створення тимчасового каталогу.
    :type tmpdir: py.path.local
    """
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(str(file), "Hello, World!")
    content = FileProcessor.read_from_file(str(file))
    assert content == "Hello, World!"

def test_write_large_data(tmpdir):
    """
    Тестує запис та читання великого обсягу даних (1 МБ).

    :param tmpdir: Фікстура pytest для створення тимчасового каталогу.
    :type tmpdir: py.path.local
    """
    file = tmpdir.join("large_testfile.txt")
    large_data = "A" * 10**6  # 1 МБ даних
    FileProcessor.write_to_file(str(file), large_data)
    content = FileProcessor.read_from_file(str(file))
    assert content == large_data

def test_write_empty_string(tmpdir):
    """
    Тестує запис та читання порожнього рядка.

    :param tmpdir: Фікстура pytest для створення тимчасового каталогу.
    :type tmpdir: py.path.local
    """
    file = tmpdir.join("empty_testfile.txt")
    FileProcessor.write_to_file(str(file), "")
    content = FileProcessor.read_from_file(str(file))
    assert content == ""

def test_file_not_found():
    """
    Тестує, чи правильно піднімається виняток FileNotFoundError, коли файл не існує.
    """
    with pytest.raises(FileNotFoundError):
        FileProcessor.read_from_file("non_existent_file.txt")
