from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.enums import UserRoleChoices
from ..enums import ChartType
from . import StatsTestCaseHelperMixin


class UserStatsViewSetAPITestCase(StatsTestCaseHelperMixin, APITestCase):
    """
    Test case for user statistics API endpoints.

    This class tests the API endpoints for gathering user statistics, including daily user registration counts
    and user counts by role. It ensures that these endpoints are accessible only to admin users and return the
    expected data format and response codes.
    """
    #: The number of users to generate for testing
    size = 20

    def setUp(self) -> None:
        """
        Set up the test environment before each test method.
        """
        # Generate an admin user for accessing protected stats endpoints
        self.admin_user = self.generate_user(
            role=UserRoleChoices.ADMIN,
            is_superuser=True,
            is_staff=True
        )
        # Generate a standard user for testing access restrictions
        self.custom_user = self.generate_user()
        # Generate a set of users for statistics
        self.generate_users(size=self.size)

    def test_users_daily_count(self):
        """
        Test the endpoint for getting daily user registration counts.
        """
        url = reverse("stats:users-daily-count")

        # Authenticate as the admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.admin_user))

        # Request the daily user counts
        response = self.client.get(url, format='json')

        # Ensure the request was successful and returned data in the expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['extra']['chart'], ChartType.LINE)
        self.assertTrue(response.data['results'][0]['count'] == self.size + 1)  # to add the user itself

        # Logout the user
        self.client.logout()

    def test_users_daily_count_with_non_admin(self):
        """
        Test that non-admin users are forbidden from accessing daily user registration counts.
        """
        url = reverse("stats:users-daily-count")

        # Authenticate as a non-admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.custom_user))

        # Request the daily user counts
        response = self.client.get(url, format='json')

        # Ensure the request is forbidden for non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Logout the user
        self.client.logout()

    def test_users_role_count(self):
        """
        Test the endpoint for getting user counts by role.
        """
        url = reverse("stats:users-role-count")

        # Authenticate as the admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.admin_user))

        # Request the user counts by role
        response = self.client.get(url, format='json')

        # Ensure the request was successful and returned data in the expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['extra']['chart'], ChartType.PIE)

        # Logout the user
        self.client.logout()

    def test_users_role_with_non_admin(self):
        """
        Test that non-admin users are forbidden from accessing user counts by role.
        """
        url = reverse("stats:users-role-count")

        # Authenticate as a non-admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.custom_user))

        # Request the user counts by role
        response = self.client.get(url, format='json')

        # Ensure the request is forbidden for non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Logout the user
        self.client.logout()


class ProfileStatsViewSetAPITestCase(StatsTestCaseHelperMixin, APITestCase):
    """
    Test case for profile statistics API endpoints.

    This class tests the API endpoints for gathering profile statistics, including daily profile creation counts,
    profiles by interest, and profiles by reason for joining. It ensures that these endpoints are accessible only
    to admin users and return the expected data format and response codes.
    """
    #: The number of user profiles to generate for testing
    size = 20

    def setUp(self) -> None:
        """
        Set up the test environment before each test method.
        """
        # Generate an admin user for accessing protected stats endpoints
        self.admin_user = self.generate_user(
            role=UserRoleChoices.ADMIN,
            is_superuser=True,
            is_staff=True
        )
        # Generate a standard user for testing access restrictions
        self.custom_user = self.generate_user()

        # Generate a set of user profiles for statistics
        self.generate_users(size=self.size)

    def test_profiles_daily_count(self):
        """
        Test the endpoint for getting daily profile creation counts.
        """
        url = reverse("stats:profiles-daily-count")

        # Authenticate as the admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.admin_user))

        # Request the daily profile counts
        response = self.client.get(url, format='json')

        # Ensure the request was successful and returned data in the expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['extra']['chart'], ChartType.LINE)

    def test_profiles_daily_count_with_non_admin(self):
        """
        Test that non-admin users are forbidden from accessing daily profile counts.
        """
        url = reverse("stats:profiles-daily-count")

        # Authenticate as a non-admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.custom_user))

        # Request the daily profile counts
        response = self.client.get(url, format='json')

        # Ensure the request is forbidden for non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profiles_interest_count(self):
        """
        Test the endpoint for getting profile counts by interest.
        """
        url = reverse("stats:profiles-interest-count")

        # Authenticate as the admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.admin_user))

        # Request the profile counts by interest
        response = self.client.get(url, format='json')

        # Ensure the request was successful and returned data in the expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['extra']['chart'], ChartType.PIE)

    def test_profiles_interest_count_with_non_admin(self):
        """
        Test that non-admin users are forbidden from accessing profile counts by interest.
        """
        url = reverse("stats:profiles-interest-count")

        # Authenticate as a non-admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.custom_user))

        # Request the profile counts by interest
        response = self.client.get(url, format='json')

        # Ensure the request is forbidden for non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profiles_reason_count(self):
        """
        Test the endpoint for getting profile counts by reason for joining.
        """
        url = reverse("stats:profiles-reason-count")

        # Authenticate as the admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.admin_user))

        # Request the profile counts by reason for joining
        response = self.client.get(url, format='json')

        # Ensure the request was successful and returned data in the expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['extra']['chart'], ChartType.PIE)

    def test_profiles_reason_count_with_non_admin(self):
        """
        Test that non-admin users are forbidden from accessing profile counts by reason for joining.
        """
        url = reverse("stats:profiles-reason-count")

        # Authenticate as a non-admin user
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.custom_user))

        # Request the profile counts by reason for joining
        response = self.client.get(url, format='json')

        # Ensure the request is forbidden for non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
