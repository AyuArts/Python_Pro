from django.test import TestCase
from users.models import CustomUser

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="password123", age=25)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.age, 25)
        self.assertTrue(user.check_password("password123"))
