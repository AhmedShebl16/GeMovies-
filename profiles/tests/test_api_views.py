from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.enums import UserRoleChoices
from ..models import Profile
from . import ProfileTestHelperMixin


User = get_user_model()


class ProfileViewSetAPITestCase(ProfileTestHelperMixin, APITestCase):
    """
    Test case for profile-related API endpoints.

    This class tests the API functionality related to user profiles, including retrieving, updating,
    and listing profiles. It ensures that authenticated users can access and modify their own profile
    information while enforcing proper permissions for accessing and modifying other users' profiles.
    """

    exclude = ('user', 'date_of_birth', 'create_at', 'update_at')

    def setUp(self):
        """
        Set up the test environment before each test method.
        """
        # Generate an active user and set up authentication
        self.user = self.generate_user(is_active=True)
        self.generate_users(is_active=True)
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))

    def test_retrieve_own_profile(self):
        """
        Test retrieving the authenticated user's own profile.
        """
        url = reverse('profiles:profile-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_update_own_profile_full(self):
        """
        Test fully updating the authenticated user's own profile.
        """
        url = reverse('profiles:profile-me')
        new_profile_info = self.instance_to_dict(
            self.generate_instance(save=False, user=None),
            exclude=self.get_exclude()
        )
        new_profile_info['phone_number_1'] = '+12495022991'
        new_profile_info['phone_number_2'] = '+12489895623'

        response = self.client.put(url, new_profile_info, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertModelFields(self.user.profile, response.data, exclude=self.get_exclude())

    def test_update_own_profile_partial(self):
        """
        Test partially updating the authenticated user's own profile.
        """
        url = reverse('profiles:profile-me')
        new_data = {
            'city': 'Testville',
            'country': 'Testland',
            'address': 'Street, Testville, Testland, 4567'
        }

        response = self.client.patch(url, new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertModelFields(self.user.profile, response.data, self.get_exclude())

    def test_list_profiles(self):
        """
        Test listing all active user profiles excluding the authenticated user's profile.
        """
        url = reverse('profiles:profile-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertQuerysetEqualList(
            Profile.objects.active().exclude(id=self.user.profile.id),
            response.data['results'],
            self.get_exclude()
        )

    def test_list_profiles_unauthenticated(self):
        """
        Test that unauthenticated access to list profiles is denied.
        """
        url = reverse('profiles:profile-list')
        self.client.credentials()  # Clear any existing authentication credentials
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_by_id(self):
        """
        Test retrieving a specific profile by its ID.
        """
        url = reverse('profiles:profile-detail', args=[self.user.profile.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.profile.id)

    def test_update_profile_by_id_as_admin(self):
        """
        Test that an admin user can update any profile.
        """
        admin_user = self.generate_user(is_active=True, role=UserRoleChoices.ADMIN, is_superuser=True, is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(admin_user))

        url = reverse('profiles:profile-detail', args=[self.user.profile.id])
        new_city = 'Testville'
        response = self.client.patch(url, {'city': new_city}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.city, new_city)

    def test_update_another_user_profile(self):
        """
        Test that a non-admin user cannot update another user's profile.
        """
        another_user = self.generate_user(role=UserRoleChoices.CUSTOMER)
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(another_user))

        url = reverse('profiles:profile-detail', args=[self.user.profile.id])
        response = self.client.patch(url, {'city': 'Testville'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
