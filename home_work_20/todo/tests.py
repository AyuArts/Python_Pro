from home_work_20.base_test_case import BaseTestCase
from .forms import TaskForm
from .serializers import TaskSerializer


class TaskFormTest(BaseTestCase):
    def test_is_valid_data(self):
        """Проверка валидности данных формы"""
        form = TaskForm(data=self.get_valid_data(name_data="task"))
        self.assertTrue(form.is_valid(), "Форма должна быть валидной для корректных данных.")

    def test_title_max_length(self):
        """Проверка превышения длины заголовка"""
        invalid_data = self.get_valid_data(name_data="task")
        invalid_data['title'] = "t" * 101  # Превышает 100 символов
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid(), "Форма не должна быть валидной при превышении длины заголовка.")
        self.assertIn('title', form.errors)
        self.assertEqual(
            form.errors['title'],
            ['Ensure this value has at most 100 characters (it has 101).'],
            "Ожидалась ошибка превышения длины заголовка."
        )

    def test_invalid_data_missing_title(self):
        """Проверка формы с отсутствующим заголовком"""
        form = TaskForm(data=self.get_missing_title_data())
        self.assertFalse(form.is_valid(), "Форма не должна быть валидной при отсутствии заголовка.")
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_invalid_data_due_date_in_past(self):
        """Проверка формы с прошлой датой"""
        form = TaskForm(data=self.get_past_date_data())
        self.assertFalse(form.is_valid(), "Форма не должна быть валидной, если due_date в прошлом.")
        self.assertIn('due_date', form.errors)


class TaskSerializersTest(BaseTestCase):
    def test_is_valid_data(self):
        """Проверка валидности данных сериализатора"""
        serializer = TaskSerializer(data=self.get_valid_data(name_data="task"))
        self.assertTrue(serializer.is_valid(), "Сериализатор должен быть валидным для корректных данных.")

    def test_missing_title(self):
        """Проверка сериализатора с отсутствующим заголовком"""
        serializer = TaskSerializer(data=self.get_missing_title_data())
        self.assertFalse(serializer.is_valid(), "Сериализатор не должен быть валидным при отсутствии заголовка.")
        self.assertIn('title', serializer.errors)
        self.assertEqual(
            serializer.errors['title'],
            ['This field may not be blank.'],
            "Ожидалась ошибка для пустого поля 'title'."
        )

    def test_due_date_in_past(self):
        """Проверка сериализатора с прошлой датой"""
        serializer = TaskSerializer(data=self.get_past_date_data())
        self.assertFalse(serializer.is_valid(), "Сериализатор не должен быть валидным, если due_date в прошлом.")
        self.assertIn('due_date', serializer.errors)
