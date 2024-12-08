from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from accounts.enums import UserRoleChoices
from ..api.filters import ProfileFilter
from ..enums import GenderChoices, InterestChoices, ReasonChoices
from . import ProfileTestHelperMixin


User = get_user_model()


class ProfileFilterTestCase(ProfileTestHelperMixin, TestCase):
    """
    Test case for profile filtering functionality.

    This class tests the filtering capabilities of the `ProfileFilter` class, ensuring that profiles can be
    accurately filtered by various attributes such as first name, last name, username, email, date of birth,
    gender, interest, and reason for joining. It leverages user and profile factories to generate test data.
    """

    filter_class = ProfileFilter  # The profile filter class to test

    def setUp(self):
        """
        Set up the test environment by generating profiles with specific attributes.
        """
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.size = 5
        # Generate a number of profiles
        self.generate_instances(size=10)
        # Generate a number of users with specific first and last names, roles, and active status
        self.generate_users(
            size=self.size,
            role=UserRoleChoices.CUSTOMER,
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=True
        )

    def test_search_filter_by_first_name(self):
        """
        Test that the search filter correctly filters profiles by first name.
        """
        filter_set = self.filter_class(data={'search': self.first_name})
        # Assert that the filtered queryset contains only profiles with users having the specified first name
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(user__first_name__icontains=self.first_name))

    def test_search_filter_by_last_name(self):
        """
        Test that the search filter correctly filters profiles by last name.
        """
        filter_set = self.filter_class(data={'search': self.last_name})
        # Assert that the filtered queryset contains only profiles with users having the specified last name
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(user__last_name__icontains=self.last_name))

    def test_search_filter_by_username(self):
        """
        Test that the search filter can partially match and filter profiles by username.
        """
        filter_set = self.filter_class(data={'search': 'user'})
        # Assert that the filtered queryset is not empty, indicating that profiles have been matched by username
        self.assertGreater(len(filter_set.qs), 0)

    def test_search_filter_by_email(self):
        """
        Test that the search filter can partially match and filter profiles by email.
        """
        filter_set = self.filter_class(data={'search': 'example.com'})
        # Assert that the filtered queryset is not empty, indicating that profiles have been matched by email
        self.assertGreater(len(filter_set.qs), 0)

    def test_filter_by_date_of_birth(self):
        """
        Test that profiles can be filtered by date of birth.
        """
        date_of_birth = now().date() - timedelta(days=365 * 20)
        filter_set = self.filter_class(data={'date_of_birth': date_of_birth})
        # Assert that the filtered queryset contains only profiles with the specified date of birth
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(date_of_birth=date_of_birth))

    def test_filter_by_gender(self):
        """
        Test that profiles can be filtered by gender.
        """
        gender = GenderChoices.MALE
        filter_set = self.filter_class(data={'gender': gender})
        # Assert that the filtered queryset contains only profiles with the specified gender
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(gender=gender))

    def test_filter_by_interest(self):
        """
        Test that profiles can be filtered by interest.
        """
        interest = InterestChoices.ADVENTURER
        filter_set = self.filter_class(data={'interest': interest})
        # Assert that the filtered queryset contains only profiles with the specified interest
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(interest=interest))

    def test_filter_by_reason(self):
        """
        Test that profiles can be filtered by the reason for joining.
        """
        reason = ReasonChoices.COMMUNITY_INVOLVEMENT
        filter_set = self.filter_class(data={'reason': reason})
        # Assert that the filtered queryset contains only profiles with the specified reason for joining
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(reason=reason))
