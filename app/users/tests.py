"""
This is a file with tests for users application in it there is a class with tests for each viewport.

The setUp function will occur in each test class,
it contains all actions that will take place before the start of each test in the class.
"""
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from plagigram import settings
from users import views


class LoginUserViewTest(TestCase):
    """This is the class for the (LoginUser) view tests."""

    def setUp(self):
        """This function creates user."""
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.url = reverse('users:login')

    def test_login_view_uses_correct_template(self):
        """This test verifies that the login page is using the correct template for display."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_renders_form(self):
        """This test checks if the correct forms are used when creating a page."""
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], views.LoginUserForm)

    def test_login_successful(self):
        """This test redirects the user to the home page after entering the correct data."""
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))

    def test_login_unsuccessful(self):
        """This test tests the error output when data is entered incorrectly."""
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Please enter a correct username and password.'
                                      ' Note that both fields may be case-sensitive.')


class RegisterUserViewTest(TestCase):
    """This is the class for the (RegisterUser) view tests."""

    def setUp(self):
        self.url = reverse('users:register')

    def test_register_view_uses_correct_template(self):
        """This test verifies that the register page is using the correct template for display."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_renders_form(self):
        """This test checks if the correct forms are used when creating a page."""
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], views.RegisterUserForm)

    def test_register_successful(self):
        """This test checks that after successful registration the user will be redirected to the login page."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(reverse_lazy('users:login'), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register_unsuccessful(self):
        """
        This test verifies that if a registration error occurs,
        the user will remain on the same page and will receive an error.
        """
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
    """This is the class for the (ProfileUser) view tests."""

    def setUp(self):
        """This function creates and registers a user."""
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client.login(username='testuser', password='testpassword')
        self.url = reverse_lazy('users:profile')

    def test_profile_user_view_uses_correct_template(self):
        """This test verifies that the profile page is using the correct template for display."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_renders_form(self):
        """This test checks if the correct forms are used when creating a page."""
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], views.ProfileUserForm)

    def test_profile_user_successful_update(self):
        """This test verifies that the profile has been successfully updated."""
        data = {
            'avatar': settings.DEFAULT_USER_IMAGE,
            'biography': 'Updated biography text',
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)


class UserProfileViewTest(TestCase):
    """This is the class for the (user_profile) view tests."""

    def setUp(self):
        """This function creates and registers a user."""
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_user_profile_view_uses_correct_template(self):
        """This test verifies that the users profile page is using the correct template for display."""
        url = reverse('users:user_profile', args=['testuser'])  # Getting the URL for the user profile

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/user_profile.html')

    def test_user_profile_view_returns_404_for_nonexistent_user(self):
        """This test checks that the code should be 404 when searching for a non-existent user."""
        url = reverse('users:user_profile', args=['nonexistentuser'])  # Getting the URL for a non-existent user profile

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_profile_view_returns_correct_data(self):
        """This test verifies that the user page returns the expected data."""
        url = reverse('users:user_profile', args=['testuser'])  # Getting the URL for the user profile

        response = self.client.get(url)

        # Verify that the response contains the expected content
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Профиль пользователя')
