from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from ..enums import UserRoleChoices
from . import GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin


User = get_user_model()


class CustomUserManagerTestCase(GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin,
                                TestCase):
    """
    Test case for custom user model manager methods.

    This class tests the custom manager methods defined in the custom user model, including creating users,
    superusers, and various queryset filters like active users and excluding admin users. It ensures that
    the custom user model behaves as expected under various scenarios, such as handling null values for
    essential fields or ensuring superuser properties are correctly set.
    """
    model = User

    def test_create_user(self):
        """
        Test the creation of a standard user with specified role and password.
        """
        user_password = 'password123'
        user = self.generate_user(role=UserRoleChoices.CUSTOMER, password=user_password)
        self.assertEqual(user.role, UserRoleChoices.CUSTOMER)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(user_password))

    def test_create_user_raises_exception_when_username_is_null(self):
        """
        Test that creating a user with a null username raises an IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            self.generate_user(username=None)

    def test_create_user_raises_exception_when_role_is_null(self):
        """
        Test that creating a user with a null role raises a ValueError.
        """
        user = self.generate_user(save=False, role=None)
        user_info = self.instance_to_dict(user)
        with self.assertRaises(ValueError):
            self.get_model().objects.create_user(**user_info)

    def test_create_superuser(self):
        """
        Test the creation of a superuser with specific role and properties.
        """
        user_password = 'password123'
        admin_user = self.generate_user(role=UserRoleChoices.ADMIN, is_superuser=True, password=user_password)
        self.assertEqual(admin_user.role, UserRoleChoices.ADMIN)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.terms_and_condition)

    def test_create_superuser_raises_exception_when_is_staff_is_not_true(self):
        """
        Test that creating a superuser without is_staff set to True raises a ValueError.
        """
        user = self.generate_user(role=UserRoleChoices.ADMIN, is_staff=False)
        user_info = self.instance_to_dict(user)
        with self.assertRaises(ValueError):
            self.get_model().objects.create_user(**user_info)

    def test_create_superuser_raises_exception_when_is_superuser_is_not_true(self):
        """
        Test that creating a superuser without is_superuser set to True raises a ValueError.
        """
        user = self.generate_user(role=UserRoleChoices.ADMIN, is_superuser=False)
        user_info = self.instance_to_dict(user)
        with self.assertRaises(ValueError):
            self.get_model().objects.create_user(**user_info)

    def test_active(self):
        """
        Test the active queryset method for filtering active users.
        """
        size = 10
        self.generate_users(size=size)
        self.assertQuerysetEqual(
            self.get_model().objects.active(),
            self.get_model().objects.filter(is_active=True),
            ordered=False
        )

    def test_exclude_admin(self):
        """
        Test the exclude_admin queryset method for filtering out admin users.
        """
        size = 10
        self.generate_users(size=size)
        self.assertQuerysetEqual(
            self.get_model().objects.exclude_admin(),
            self.get_model().objects.filter(is_active=True).exclude(role=UserRoleChoices.ADMIN),
            ordered=False
        )


class UserModelTestCase(GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin, TestCase):
    """
    Test case for the User model.

    This class covers various aspects of the User model, including the uniqueness constraints for email and username,
    the string representation of a user, and certain model constraints such as acceptance of terms and conditions
    and role requirements for superusers.
    """
    model = User

    def test_email_uniqueness(self):
        """
        Test that attempting to create a user with an email that already exists raises an IntegrityError.
        """
        email = 'user@gmail.com'
        self.generate_user(email=email)
        with self.assertRaises(IntegrityError):
            self.generate_user(email=email)

    def test_username_uniqueness(self):
        """
        Test that attempting to create a user with a username that already exists raises an IntegrityError.
        """
        username = 'user@gmail.com'
        self.generate_user(username=username)
        with self.assertRaises(IntegrityError):
            self.generate_user(username=username)

    def test_string_representation(self):
        """
        Test the string representation of a user model is as expected (user's email).
        """
        user = self.generate_user()
        self.assertEqual(str(user), user.email)

    def test_check_constraint_terms_and_conditions_must_be_true(self):
        """
        Test that creating a user without accepting terms and conditions raises an IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            self.generate_user(terms_and_condition=False)

    def test_check_constraint_superuser_must_be_admin(self):
        """
        Test that creating a superuser with a role other than admin raises a ValueError.
        """
        user = self.generate_user(save=False, role=UserRoleChoices.OTHER)
        user_info = self.instance_to_dict(user)
        with self.assertRaises(ValueError):
            self.get_model().objects.create_superuser(**user_info)
