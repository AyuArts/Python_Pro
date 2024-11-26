from home_work_20.base_test_case import BaseTestCase

from .serializers import UserSerializer


class UsersSerializerTest(BaseTestCase):
    def test_valid_data(self):
        serializer = UserSerializer(data=self.get_valid_data(name_data="user"))
        self.assertTrue(serializer.is_valid(), "Сериализатор должен быть валидным для корректных данных.")

    def test_invalid_data(self):
        invalid_data = self.get_valid_data(name_data="user")["username"] = ""
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())



