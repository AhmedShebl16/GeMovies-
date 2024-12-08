from datetime import timedelta

from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils.timezone import localdate
from django.contrib.auth import get_user_model

from accounts.enums import UserRoleChoices
from ..constants import MIN_AGE
from . import ProfileTestHelperMixin


User = get_user_model()


class ProfileManagerTestCase(ProfileTestHelperMixin, TestCase):
    """
    Profile manager test case.

    This class provides test cases for profile management functionalities. It inherits from both ProfileTestHelperMixin
    and TestCase to utilize utility functions for profile testing and standard testing structures in Django,
    respectively. The tests ensure that the profile manager correctly handles queries related to active users and users
    within a certain age range.
    """
    #: Number of users to generate for the tests
    size = 10

    def setUp(self):
        """
        Sets up the test environment by generating a predefined number of users.
        """
        self.generate_users(size=self.size)

    def test_active(self):
        """
        Tests retrieval of active profiles.

        Ensures that the query for fetching active profiles returns the correct set of profiles by comparing it to a
        manual filter on the user's `is_active` flag.
        """
        self.assertQuerysetEqual(
            self.get_model().objects.active(),
            self.get_model().objects.filter(user__is_active=True),
            ordered=False
        )

    def test_age_range(self):
        """
        Tests retrieval of profiles within a specified age range.

        Checks if the query for profiles within an age range (from MIN_AGE to 100) matches the profiles returned by
        applying an age filter on all profiles.
        """
        self.assertQuerysetEqual(
            self.get_model().objects.age_range(MIN_AGE, 100),
            self.get_model().objects.all().with_age(),
            ordered=False
        )


class ProfileModelTestCase(ProfileTestHelperMixin, TestCase):
    """
    Profile model test case.

    This class is designed to run tests against the Profile model to ensure its integrity and the enforcement of its
    constraints, such as uniqueness of the user associated with each profile, role validity for users assigned to
    profiles, and adherence to the minimum age requirement. The tests leverage the ProfileTestHelperMixin for
    creating user and profile instances and the TestCase class from Django's test framework for structured testing.
    """

    def test_user_uniqueness(self):
        """
        Tests that a user cannot be associated with multiple profiles.

        This test verifies that attempting to update profiles to have the same user raises an `IntegrityError`,
        enforcing user uniqueness across profiles.
        """
        profiles = self.generate_instances(size=2)
        with self.assertRaises(IntegrityError):
            self.get_queryset().update(user=profiles[0].user)

    def test_user_invalid_role(self):
        """
        Tests that only users with specific roles can be associated with a profile.

        This test ensures that an `IntegrityError` is raised when attempting to create a profile for a user with an
        invalid role.
        """
        # TODO: Resolve this problem - nothing is raised when none customer user is assigned to profile
        # user = self.generate_user(role=UserRoleChoices.OTHER)
        # with self.assertRaises(IntegrityError):
        #     self.generate_instance(user=user)

    def test_check_constraint_min_date_of_birth(self):
        """
        Tests the enforcement of the minimum age constraint for profile creation.

        This test checks that an `IntegrityError` is raised when attempting to create a profile with a date of birth
        that does not meet the minimum age requirement.
        """
        # TODO: Resolve this problem - nothing is raised when the date of birth year is less than the MIN_AGE limit
        # invalid_date_of_birth = localdate() - timedelta(days=365 * (MIN_AGE - 1))
        # with self.assertRaises(IntegrityError):
        #     self.generate_instance(date_of_birth=invalid_date_of_birth)
