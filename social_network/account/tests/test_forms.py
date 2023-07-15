from django.test import TestCase
from account.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='ali', email='ali@gmail.com', password='qwerty')

    def test_valid_data(self):
        form = UserRegistrationForm(data={'username': 'amin', 'email': 'amin@gmail.com',
                                          'password1': 'qwe', 'password2': 'qwe'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_email(self):
        form = UserRegistrationForm(data={'username': 'amin', 'email': 'ali@gmail.com',
                                          'password1': 'qwe', 'password2': 'qwe'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_unmatched_password(self):
        form = UserRegistrationForm(data={'username': 'armin', 'email': 'armin@gmail.com',
                                          'password1': 'qwe', 'password2': 'qie'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)

    def test_username(self):
        form = UserRegistrationForm(data={'username': 'ali', 'email': 'ali2@gmail.com',
                                          'password1': 'ewq', 'password2': 'ewq'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))
