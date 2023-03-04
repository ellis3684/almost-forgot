from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def get_users_count():
    """Get number of total users in database"""
    return get_user_model().objects.all().count()


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """Create user with username and password"""
        cls.existing_user = User.objects.create_user(
            'alreadyexistinguser',
            password='ivebeenhere456'
        )

    def test_register_get_status_code(self):
        """Getting the user registration page succeeds with status code 200"""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_post_status_code(self):
        """Registering a user succeeds with status code 200"""
        response = self.client.post('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
        """Registering a new user increments total user count by 1"""
        users_before_register = get_users_count()
        response = self.client.post('/register/', data={
            'username': 'hiimanewuser',
            'password1': 'justtesting123',
            'password2': 'justtesting123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        users_after_register = get_users_count()
        self.assertEqual(users_before_register + 1, users_after_register)

    def test_password_confirmation_failure(self):
        """Password confirmation that doesn't match password should fail to generate new user"""
        users_before_register = get_users_count()
        response = self.client.post('/register/', data={
            'username': 'hiimanewuser',
            'password1': 'justtesting123',
            'password2': 'thisiswrong321',
        })
        self.assertEqual(response.status_code, 200)
        users_after_register = get_users_count()
        self.assertEqual(users_before_register, users_after_register)

    def test_register_user_exists(self):
        """Attempting to register a user that already exists fails to generate new user"""
        users_before_register = get_users_count()
        exists = self.existing_user
        response = self.client.post('/register/', data={
            'username': exists.username,
            'password1': exists.password,
            'password2': exists.password,
        })
        users_after_register = get_users_count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users_before_register, users_after_register)
