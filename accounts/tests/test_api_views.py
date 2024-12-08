from datetime import timedelta

from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from . import GenericTestCaseHelperMixin, UserTestCaseHelperMixin


User = get_user_model()


class JWTAPITestCase(UserTestCaseHelperMixin, APITestCase):
    """
    Test case for JWT (JSON Web Token) API endpoints.

    This class tests the JWT authentication flow, including token creation, refresh, and verification, to ensure the
    authentication system is functioning correctly. It uses the UserTestCaseHelperMixin to generate user instances for
    authentication tests.
    """

    def test_jwt_create(self):
        """
        Tests the JWT create endpoint to ensure it returns a valid access and refresh token upon user login.
        """
        # Endpoint for creating JWT
        url = reverse("accounts:jwt-create")

        # Create a new user
        user = self.generate_user(password='password')

        # User login credentials
        data = {
            "email": user.email,
            "password": "password",
        }

        # Make a POST request to the JWT create endpoint
        response = self.client.post(url, data)

        # Assert that the response status code is 200 OK and both tokens are present in the response data
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["refresh"])
        self.assertIsNotNone(response.data["access"])

    def test_jwt_refresh(self):
        """
        Tests the JWT refresh endpoint to ensure it returns a new access token using a valid refresh token.
        """
        # Endpoint for refreshing JWT
        url = reverse("accounts:jwt-refresh")

        # Create a new user
        user = self.generate_user()

        # Generate a refresh token
        refresh = self.get_refresh_token(user)

        # Data payload with refresh token
        data = {
            'refresh': str(refresh)
        }

        # Make a POST request to the JWT refresh endpoint
        response = self.client.post(url, data)

        # Assert that the response status code is 200 OK and new tokens are present in the response data
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["refresh"])
        self.assertIsNotNone(response.data["access"])

    def test_jwt_verify(self):
        """
        Tests the JWT verify endpoint to ensure it validates a given access token successfully.
        """
        # Endpoint for verifying JWT
        url = reverse("accounts:jwt-verify")

        # Create a new user
        user = self.generate_user()

        # Generate an access token
        access = self.get_access_token(user)

        # Data payload with access token
        data = {
            'token': str(access)
        }

        # Make a POST request to the JWT verify endpoint
        response = self.client.post(url, data)

        # Assert that the response status code is 200 OK, indicating the token is valid
        self.assertTrue(response.status_code, status.HTTP_200_OK)

    def test_expired_access_token_and_refresh(self):
        """
        Tests the JWT refresh mechanism with an expired access token, ensuring a new access token can be obtained.
        """
        # Endpoint for refreshing JWT
        url = reverse("accounts:jwt-refresh")

        # Endpoint protected by JWT authentication
        protected_url = reverse('accounts:user-me')

        # Create a new user
        user = self.generate_user()

        # Set the Authorization header with an expired access token
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user, timedelta(minutes=-10)))
        # Attempt to access a protected endpoint with the expired access token
        response = self.client.get(protected_url)
        # Assert that the response status code is 401 Unauthorized due to expired token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Use a valid refresh token to obtain a new access token
        refresh = self.get_refresh_token(user)
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data)
        # Assert that the refresh operation was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the new access token from the response
        new_access_token = response.data['access']
        # Set the Authorization header with the new access token
        self.client.credentials(HTTP_AUTHORIZATION=self.format_auth_header(new_access_token))
        # Attempt to access the protected endpoint with the new access token
        response = self.client.get(protected_url)
        # Assert that the access is now granted with the new token
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetAPITestCase(GenericTestCaseHelperMixin, UserTestCaseHelperMixin, APITestCase):
    """
    Test case for user-related API endpoints in the 'accounts' namespace.

    This class covers a wide range of API interactions related to user management, including listing users, creating
    new users, retrieving/updating/deleting user details by ID, handling user activation, password resets, and email
    updates. It leverages the UserTestCaseHelperMixin for user creation and authentication header setup.
    """

    def test_get_users_list(self):
        """
        Test retrieving a list of users through the API.
        """
        url = reverse('accounts:user-list')

        user = self.generate_user()

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Test creating a new user through the API.
        """
        url = reverse("accounts:user-list")

        user_info = self.generate_user(save=False)
        data = self.instance_to_dict(user_info, exclude=('id', 'last_login'))

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=response.data['id'])

        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.role, data["role"])
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)
        self.assertTrue(user.terms_and_condition)
        self.assertTrue(user.check_password(data["password"]))

    def test_get_user_by_id(self):
        """
        Test retrieving user details by ID through the API.
        """
        self.generate_users(size=2)

        user = User.objects.first()
        url = reverse('accounts:user-detail', args=[user.id])

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)

    def test_update_user_by_id(self):
        """
        Test updating user details by ID through the API.
        """
        user = self.generate_user()

        url = reverse('accounts:user-detail', args=[user.id])

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.patch(url, {'first_name': 'new_first_name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)
        self.assertNotEqual(response.data['first_name'], user.first_name)

    def test_delete_user_by_id(self):
        """
        Test deleting a user by ID through the API.
        """
        user = self.generate_user(password='password')

        url = reverse('accounts:user-detail', args=[user.id])

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.delete(url, data={'current_password': 'password'})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_user_me(self):
        """
        Test retrieving the authenticated user's details through the API.
        """
        url = reverse('accounts:user-me')

        self.generate_users(save=True, size=2)

        user = User.objects.first()

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)

    def test_update_user_me(self):
        """
        Test updating the authenticated user's details through the API.
        """
        url = reverse('accounts:user-me')

        user = self.generate_user()

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.patch(url, {'first_name': 'new_first_name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)
        self.assertNotEqual(response.data['first_name'], user.first_name)

    def test_delete_user_me(self):
        """
        Test deleting the authenticated user's account through the API.
        """
        url = reverse('accounts:user-me')

        user = self.generate_user(password='password')

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.delete(url, data={'current_password': 'password'})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_activation(self):
        """
        Test the user account activation process through the API.
        """
        url = reverse('accounts:user-activation')

        user = self.generate_user(is_active=False)

        data = {
            'uid': self.encode_user_pk(user.pk),
            'token': self.token_generator(user)
        }

        response = self.client.post(url, data=data)

        # Refresh user instance to get updated values from the database
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(user.is_active)

    def test_resend_activation(self):
        """
        Test the resend activation email functionality through the API.
        """
        url = reverse('accounts:user-resend-activation')

        user = self.generate_user(is_active=False)

        response = self.client.post(url, {'email': user.email})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])

    def test_reset_email(self):
        """
        Test the email reset functionality through the API.
        """
        url = reverse('accounts:user-reset-username')

        user = self.generate_user()

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        data = {
            'email': user.email,
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])

    def test_reset_email_confirm(self):
        """
        Test confirming the email reset process through the API.
        """
        url = reverse('accounts:user-reset-username-confirm')

        user = self.generate_user()

        new_email = 'new_email@gmail.com'
        data = {
            'uid': self.encode_user_pk(user.pk),
            'token': self.token_generator(user),
            'new_email': new_email
        }

        response = self.client.post(url, data)

        # Refresh the user instance to get updated values
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.email, new_email)

    def test_reset_password(self):
        """
        Test the password reset request functionality through the API.
        """
        url = reverse('accounts:user-reset-password')

        user = self.generate_user()

        response = self.client.post(url, {'email': user.email})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])

    def test_reset_password_confirm(self):
        """
        Test confirming the password reset process through the API.
        """
        url = reverse('accounts:user-reset-password-confirm')

        user = self.generate_user()

        new_password = 'new_password_123'
        data = {
            'uid': self.encode_user_pk(user.pk),
            'token': self.token_generator(user),
            "new_password": new_password
        }

        response = self.client.post(url, data)

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(user.check_password(new_password))

    def test_set_email(self):
        """
        Test updating the authenticated user's email through the API.
        """
        url = reverse('accounts:user-set-username')

        user_password = 'password123'
        user = self.generate_user(password=user_password)

        new_email = 'new_email@gmail.com'
        data = {
            "current_password": user_password,
            "new_email": new_email
        }

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.post(url, data)

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.email, new_email)

    def test_set_password(self):
        """
        Test updating the authenticated user's password through the API.
        """
        url = reverse('accounts:user-set-password')

        user_password = 'password123'
        user = self.generate_user(password=user_password)

        new_password = 'newpassword321'
        data = {
            "new_password": new_password,
            "re_new_password": new_password,
            "current_password": user_password
        }

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user))

        response = self.client.post(url, data)

        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(user.check_password(new_password))
