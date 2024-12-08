from unittest.mock import MagicMock

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from ..api.views import UserViewSet
from ..signals import user_deactivated
from . import UserTestCaseHelperMixin


User = get_user_model()


class UserDeactivationSignalAPITestCase(UserTestCaseHelperMixin, APITestCase):
    """
    API test case for user deactivation signals.

    This test case ensures that the `user_deactivated` signal is correctly emitted upon user deactivation through
    various actions, such as setting a new username or confirming a username reset. It uses the UserTestCaseHelperMixin
    to generate user instances and sets up a mock signal receiver to intercept and assert signal emissions.
    """

    def setUp(self):
        """
        Set up the test environment before each test method.

        This includes generating a user instance, setting up a user password, and connecting a mock signal receiver
        to the `user_deactivated` signal.
        """
        # Define a password for the user
        self.user_password = 'password123'
        # Generate a user instance with the specified password
        self.user = self.generate_user(password=self.user_password)
        # Create a mock receiver for the signal
        self.mock_receiver = MagicMock()
        # Connect the mock receiver to the `user_deactivated` signal
        user_deactivated.connect(self.mock_receiver)

    def tearDown(self):
        """
        Clean up after each test method.

        This includes disconnecting the mock signal receiver from the `user_deactivated` signal to prevent any
        interference with other tests.
        """
        # Disconnect the mock receiver
        user_deactivated.disconnect(self.mock_receiver)

    def test_user_deactivation_signal_with_set_username_action(self):
        """
        Test that the `user_deactivated` signal is emitted when a user's username is set to a new value.
        """
        url = reverse('accounts:user-set-username')

        new_email = 'new_email@gmail.com'
        data = {
            "current_password": self.user_password,
            "new_email": new_email
        }

        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))

        response = self.client.post(url, data)

        # Assert that the response status code is 204 No Content, indicating the request was processed successfully.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Refresh the user instance from the database to ensure we have the latest data, particularly after any changes
        # made during the test.
        self.user.refresh_from_db()

        # Check that the mock signal receiver was called at least once.
        self.assertTrue(self.mock_receiver.called)
        # Ensure the mock signal receiver was called exactly once.
        self.assertEqual(self.mock_receiver.call_count, 1)

        # Retrieve the sender argument passed to the signal from the mock receiver's call arguments.
        sender = self.mock_receiver.call_args.kwargs['sender']
        # Retrieve the user argument passed to the signal from the mock receiver's call arguments.
        called_user = self.mock_receiver.call_args.kwargs['user']

        # Verify that the user instance in the signal's call arguments matches the test user.
        self.assertEqual(called_user, self.user)
        # Assert that the sender of the signal is the UserViewSet, as expected.
        self.assertEqual(sender, UserViewSet)

    def test_user_deactivation_signal_with_reset_username_confirm_action(self):
        """
        Test that the `user_deactivated` signal is emitted upon confirming a username reset action.
        """
        url = reverse('accounts:user-reset-username-confirm')

        new_email = 'new_email@gmail.com'
        data = {
            'uid': self.encode_user_pk(self.user.pk),
            'token': self.token_generator(self.user),
            'new_email': new_email
        }

        response = self.client.post(url, data)

        # Assert that the response status code is 204 No Content, indicating the request was processed successfully.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Refresh the user instance from the database to ensure we have the latest data, particularly after any changes
        # made during the test.
        self.user.refresh_from_db()

        # Check that the mock signal receiver was called at least once.
        self.assertTrue(self.mock_receiver.called)
        # Ensure the mock signal receiver was called exactly once.
        self.assertEqual(self.mock_receiver.call_count, 1)

        # Retrieve the sender argument passed to the signal from the mock receiver's call arguments.
        sender = self.mock_receiver.call_args.kwargs['sender']
        # Retrieve the user argument passed to the signal from the mock receiver's call arguments.
        called_user = self.mock_receiver.call_args.kwargs['user']

        # Verify that the user instance in the signal's call arguments matches the test user.
        self.assertEqual(called_user, self.user)
        # Assert that the sender of the signal is the UserViewSet, as expected.
        self.assertEqual(sender, UserViewSet)
