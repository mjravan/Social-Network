from django.test import TestCase, Client
from django.urls import reverse
from account.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse('account:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')
        self.failUnless(response.context['form'], UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(reverse('account:user_register'), data={'username': 'ken', 'email': 'kar@gmail.com',
                                                                            'password1': 'ken', 'password2': 'ken'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('account:user_register'), data={'username': 'kar', 'email': 'invalid_email',
                                                                            'password1': 'qwer', 'password2': 'qwe'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='email', errors=['Enter a valid email address.'])


class TestUserLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(username='root', password='root')
        self.client = Client()

    def test_user_login_GET(self):
        response = self.client.get(reverse('account:user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        self.failUnless(response.context['form'], UserLoginForm)

    def test_user_login_POST_valid(self):
        response = self.client.post(reverse('account:user_login'), data={'username': 'root', 'password': 'root'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

    def test_user_login_POST_invalid(self):
        response = self.client.post(reverse('account:user_login'), data={'username': 'amir', 'password': 'root'})
        self.assertWarnsMessage(response, 'username or password is wrong')

    def test_user_login_POST_invalid_data(self):
        response = self.client.post(reverse('account:user_login'), data={'username': '',
                                                                         'password': 'root'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='username', errors='This field is required.')


class TestUserLogOut(TestCase):
    def setUp(self):
        User.objects.create_user(username='root', password='root')
        self.client = Client()
        self.client.login(username='root', password='root')

    def test_user_logout_GET(self):
        response = self.client.get(reverse('account:user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        self.assertRaisesMessage(response, 'you logged out successfully')
