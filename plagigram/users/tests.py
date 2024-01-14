from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from plagigram import settings
from users import views


class LoginUserViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.url = reverse('users:login')

    def test_login_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_renders_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], views.LoginUserForm)

    def test_login_successful(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))

    def test_login_unsuccessful(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Please enter a correct username and password.'
                                      ' Note that both fields may be case-sensitive.')


class RegisterUserViewTest(TestCase):
    def setUp(self):
        # Устанавливаем URL для вьюхи
        self.url = reverse('users:register')

    def test_register_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_renders_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], views.RegisterUserForm)

    def test_register_successful(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(reverse_lazy('users:register'), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register_unsuccessful(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'wrongpassword',  # Passwords don't match intentionally
        }
        response = self.client.post(self.url, data)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'The two password fields didn’t match.')


class ProfileUserViewTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_profile_user_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse_lazy('users:profile')

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_user_successful_update(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse_lazy('users:profile')

        data = {
            'avatar': settings.DEFAULT_USER_IMAGE,
            'biography': 'Updated biography text',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)


class UserProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_profile_view_uses_correct_template(self):
        # Log in to access the protected URL
        self.client.login(username='testuser', password='testpassword')

        # Getting the URL for the user profile
        url = reverse('users:user_profile', args=['testuser'])

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/user_profile.html')

    def test_user_profile_view_returns_404_for_nonexistent_user(self):
        # Log in to access the protected URL
        self.client.login(username='testuser', password='testpassword')

        # Getting the URL for a non-existent user profile
        url = reverse('users:user_profile', args=['nonexistentuser'])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_profile_view_returns_correct_data(self):
        # Log in to access the protected URL
        self.client.login(username='testuser', password='testpassword')

        # Getting the URL for the user profile
        url = reverse('users:user_profile', args=['testuser'])

        response = self.client.get(url)

        # Verify that the response contains the expected content
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Профиль пользователя')
