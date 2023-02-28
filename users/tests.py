from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def get_users_count():
    return get_user_model().objects.all().count()


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.existing_user = User.objects.create_user(
            'alreadyexistinguser',
            password='ivebeenhere456'
        )

    def test_register_get_status_code(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_post_status_code(self):
        response = self.client.post('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
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
