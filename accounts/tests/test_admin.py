from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage

from ..admin import CustomUserAdmin
from ..enums import UserRoleChoices
from . import ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin


User = get_user_model()


class CustomUserAdminTestCase(ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin, TestCase):
    """
    Test case for custom Django admin actions related to user activation and deactivation.

    This class extends Django's TestCase and incorporates ModelTestCaseHelperMixin and UserFactoryTestCaseHelperMixin
    to provide a robust testing environment. It specifically tests the functionality of activating and deactivating
    user accounts through custom admin actions, ensuring these operations behave as expected within the Django admin
    interface.
    """
    #: Number of users to generate for each test scenario.
    size = 5
    #: Django user model.
    model = User

    def setUp(self) -> None:
        """
        Set up the test environment by generating active and inactive user instances, configuring the request object,
        setting up Django messages, and initializing the CustomUserAdmin class.
        """
        # Generate active and inactive users
        self.generate_users(size=self.size, is_active=True)
        self.generate_users(size=self.size, is_active=False)

        # Set up the request object with an admin user
        self.request = HttpRequest()
        self.request.user = self.generate_user(role=UserRoleChoices.ADMIN)

        # Set up Django messages framework for the request
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

        # Initialize the CustomUserAdmin object with the current model and admin site
        self.model_admin = CustomUserAdmin(self.get_model(), AdminSite())

    def test_activate_users(self):
        """
        Test the 'activate_users' admin action to ensure it correctly activates all users.
        """
        # Execute the activate_users action
        self.model_admin.activate_users(self.request, self.get_queryset())

        # Assert that there are no inactive users left after the action
        self.assertEqual(self.get_queryset(is_active=False).count(), 0)

    def test_deactivate_users(self):
        """
        Test the 'deactivate_users' admin action to ensure it correctly deactivates all users.
        """
        # Execute the deactivate_users action
        self.model_admin.deactivate_users(self.request, self.get_queryset())

        # Assert that there are no active users left after the action
        self.assertEqual(self.get_queryset(is_active=True).count(), 0)
