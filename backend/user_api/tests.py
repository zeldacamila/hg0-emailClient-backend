from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser', email='testuser@domain.com', password='Testpassword123!')

    """
    Test the user API-signup, with valid user data
    """

    def test_signup(self):
        data = {
            'username': 'testuser2',
            'email': 'testuser2@domain.com',
            'password': 'Testpassword123!',
            'password2': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signup'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_exists = User.objects.filter(username='testuser2').exists()
        self.assertTrue(user_exists)
        if user_exists:
            user = User.objects.get(username='testuser2')
            self.assertEqual(user.email, 'testuser2@domain.com')
            # Ensure the password is not returned in the response
            self.assertTrue('password' not in response.data)

    """
    Test the user API-signup, with invalid user data, username is missing
    """

    def test_signup_with_existing_username(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@domain.com',
            'password': 'Testpassword123!',
            'password2': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signup'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test the user API-signup, with invalid user data, email is missing
    """

    def test_signup_with_existing_email(self):
        data = {
            'username': 'user',
            'email': 'testuser@domain.com',
            'password': 'Testpassword',
            'password2': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signup'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test the user API-signup, with invalid user data, only one password is provided
    """

    def test_signup_with_one_password(self):
        data = {
            'username': 'testuser3',
            'email': 'testuser3@domain.com',
            'password': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signup'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test the user API-signup, with invalid user data, passwords do not match
    """

    def test_signup_with_unmatching_passwords(self):
        data = {
            'username': 'testuser3',
            'email': 'testuser3@domain.com',
            'password': 'Testpassword',
            'password2': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signup'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password fields didn't match.",
                      response.data['message']['password'][0])

    """
    Test the user API-sigin, with valid user data
    """

    def test_signin(self):
        data = {
            'username': 'testuser',
            'password': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signin'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data['data'])

    """
    Test the user API-sigin, with invalid user data, username is incorrect
    """

    def test_signin_with_incorrect_username(self):
        data = {
            'username': 'testuserrrr',
            'password': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signin'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Invalid email or password. Please, check the input data and try again.", response.data['message'])

    """
    Test the user API-sigin, with invalid user data, password is incorrect
    """

    def test_signin_with_incorrect_password(self):
        data = {
            'username': 'testuser',
            'password': 'Testpassword12!'
        }
        response = self.client.post(
            reverse('auth-signin'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Invalid email or password. Please, check the input data and try again.", response.data['message'])

    """
    Test the user API-Validate token, with valid token
    """

    def test_validate_token(self):
        data = {
            'username': 'testuser',
            'password': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signin'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_validation_data = {
            'token': response.data['data']['access_token']}
        validation_response = self.client.post(
            reverse('auth-validate-token'), token_validation_data, format='json')
        self.assertEqual(validation_response.status_code, status.HTTP_200_OK)
        self.assertIn("Token is valid", validation_response.data['message'])

    """
    Test the user API-Validate token, with invalid token
    """

    def test_validate_token_with_invalid_token(self):
        data = {
            'username': 'testuser',
            'password': 'Testpassword123!'
        }
        response = self.client.post(
            reverse('auth-signin'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_validation_data = {
            'token': response.data['data']['access_token']}
        invalid_token = token_validation_data['token'] + 'invalid'
        token_validation_data['token'] = invalid_token
        validation_response = self.client.post(
            reverse('auth-validate-token'), token_validation_data, format='json')
        self.assertEqual(validation_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertIn("Token is invalid or expired",
                      validation_response.data['message'])
