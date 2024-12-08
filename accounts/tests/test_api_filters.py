from django.test import TestCase
from django.contrib.auth import get_user_model

from ..enums import UserRoleChoices
from ..api.filters import UserFilter
from . import GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin


User = get_user_model()


class UserFilterTestCase(GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserFactoryTestCaseHelperMixin,
                         TestCase):
    """
    Test case for user filtering functionality.

    This class tests the filtering capabilities of the `UserFilter` class, ensuring that users can be accurately
    filtered by various attributes such as first name, last name, username, email, and role. It leverages user factory
    methods to generate test users and applies different filter criteria to validate the filtering logic.
    """
    # Number of users to generate for each test condition
    size = 5
    # Test first name to filter by
    first_name = 'John'
    # Test last name to filter by
    last_name = 'Doe'
    # Django user model
    model = User
    # The user filter class to test
    filter_class = UserFilter

    def setUp(self):
        """
        Set up the test environment by generating users with specific first names, last names, and active status.
        """
        # Generate users with a specific first name
        self.generate_users(size=self.size, first_name=self.first_name, is_active=True)

        # Generate users with a specific last name
        self.generate_users(size=self.size, last_name=self.last_name, is_active=True)

    def test_search_filter_by_first_name(self):
        """
        Test that the search filter correctly filters users by first name.
        """
        # Apply the filter
        filter_set = self.filter_class(data={'search': self.first_name})

        # Assert that the filtered queryset contains only users with the specified first name
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(first_name=self.first_name))

    def test_search_filter_by_last_name(self):
        """
        Test that the search filter correctly filters users by last name.
        """
        # Apply the filter
        filter_set = self.filter_class(data={'search': self.last_name})

        # Assert that the filtered queryset contains only users with the specified last name
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(last_name=self.last_name))

    def test_search_filter_by_username(self):
        """
        Test that the search filter can partially match and filter users by username.
        """
        # Apply the filter with a partial username
        filter_set = self.filter_class(data={'search': 'user'})

        # Assert that the filtered queryset is not empty, indicating that users have been matched by username
        self.assertGreater(len(filter_set.qs), 0)

    def test_search_filter_by_email(self):
        """
        Test that the search filter can partially match and filter users by email.
        """
        # Apply the filter with a partial email domain
        filter_set = self.filter_class(data={'search': 'example.com'})

        # Assert that the filtered queryset is not empty, indicating that users have been matched by email
        self.assertGreater(len(filter_set.qs), 0)

    def test_filter_by_role(self):
        """
        Test that users can be filtered by their role.
        """
        # Apply the filter with a specific user role
        filter_set = self.filter_class(data={'role': UserRoleChoices.CUSTOMER})

        # Assert that the filtered queryset contains only users with the specified role
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(role=UserRoleChoices.CUSTOMER))
