from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from accounts.enums import UserRoleChoices
from accounts.factories import UserFactory
from profiles.factories import ProfileFactory
from profiles.enums import GenderChoices, InterestChoices, ReasonChoices
from ..api.filters import UserStatsFilter, ProfileStatsFilter
from . import StatsTestCaseHelperMixin


class UserStatsFilterTestCase(StatsTestCaseHelperMixin, TestCase):
    """
    Test case for user statistics filtering functionality.

    This class tests the filtering capabilities of the `UserStatsFilter` class, ensuring that users can be
    accurately filtered by attributes such as role and date joined. It leverages user factory methods to
    generate test users with specific attributes for filtering.
    """
    #: Users with first name
    first_name = 'John'
    #: Users with last name
    last_name = 'Doe'
    #: Users who joined 2 years ago
    date_joined = now() - timedelta(days=365 * 2)
    #: Specifies the factory class for creating user instances
    factory_class = UserFactory
    #: The user stats filter class to test
    filter_class = UserStatsFilter

    def setUp(self):
        """
        Set up the test environment by generating users with specific attributes.
        """
        # Generate users with a specific first name and active status
        self.generate_users(size=self.size, first_name=self.first_name, is_active=True)

        # Generate users with a specific last name, date joined, and active status
        self.generate_users(size=self.size, last_name=self.last_name, date_joined=self.date_joined, is_active=True)

    def test_filter_by_role(self):
        """
        Test that the user stats filter correctly filters users by role.
        """
        # Apply the filter with a specific user role
        filter_set = self.filter_class(data={'role': UserRoleChoices.CUSTOMER})

        # Assert that the filtered queryset contains only users with the specified role
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(**{'role': UserRoleChoices.CUSTOMER}))

    def test_filter_by_date_joined(self):
        """
        Test that the user stats filter correctly filters users by date joined.
        """
        # Apply the filter with a specific date joined
        filter_set = self.filter_class(data={'date_joined': self.date_joined})

        # Assert that the filtered queryset contains only users who joined on the specified date
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(**{'date_joined__date': self.date_joined}))


class ProfileStatsFilterTestCase(StatsTestCaseHelperMixin, TestCase):
    #: Default city for testing
    city = 'City'
    #: Default country for testing
    country = 'Country'
    #: Default address for testing
    address = 'Address'
    #: Calculate a date of birth 20 years ago from today
    date_of_birth = now().date() - timedelta(days=365 * 20)
    #: Factory class used to create profile instances for testing
    factory_class = ProfileFactory
    #: Filter class being tested
    filter_class = ProfileStatsFilter

    def setUp(self):
        """
        Set up the test environment before each test method runs.
        """
        # Store the current time for filtering by creation date
        self.now = now()
        # Generate profiles with the specified city, country, and address
        self.generate_instances(size=self.size, city=self.city, country=self.country, address=self.address)
        # Generate profiles with the specified date of birth
        self.generate_instances(size=self.size, date_of_birth=self.date_of_birth)

    def test_filter_by_gender(self):
        """
        Test filtering profiles by gender.
        """
        # Set the gender to filter by
        gender = GenderChoices.MALE
        # Initialize the filter with the selected gender
        filter_set = self.filter_class(data={'gender': gender})
        # Assert that the filtered queryset matches profiles with the specified gender
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(gender=gender))

    def test_filter_by_city(self):
        """
        Test filtering profiles by city.
        """
        # Initialize the filter with the selected city
        filter_set = self.filter_class(data={'city': self.city})
        # Assert that the filtered queryset matches profiles with the specified city
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(city=self.city))

    def test_filter_by_country(self):
        """
        Test filtering profiles by country.
        """
        # Initialize the filter with the selected country
        filter_set = self.filter_class(data={'country': self.country})
        # Assert that the filtered queryset matches profiles with the specified country
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(country=self.country))

    def test_filter_by_address(self):
        """
        Test filtering profiles by address.
        """
        # Initialize the filter with the selected address
        filter_set = self.filter_class(data={'address': self.address})
        # Assert that the filtered queryset matches profiles with the specified address
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(address=self.address))

    def test_filter_by_interest(self):
        """
        Test filtering profiles by interest.
        """
        # Set the interest to filter by
        interest = InterestChoices.ADVENTURER
        # Initialize the filter with the selected interest
        filter_set = self.filter_class(data={'interest': interest})
        # Assert that the filtered queryset matches profiles with the specified interest
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(interest=interest))

    def test_filter_by_reason(self):
        """
        Test filtering profiles by reason for joining.
        """
        # Set the reason for joining to filter by
        reason = ReasonChoices.COMMUNITY_INVOLVEMENT
        # Initialize the filter with the selected reason
        filter_set = self.filter_class(data={'reason': reason})
        # Assert that the filtered queryset matches profiles with the specified reason for joining
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(reason=reason))

    def test_filter_by_create_at(self):
        """
        Test filtering profiles by creation date.
        """
        # Initialize the filter with the creation date threshold
        filter_set = self.filter_class(data={'create_at__gte': self.now})
        # Assert that the filtered queryset matches profiles created on or after the specified date
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(create_at__gte=self.now))

    def test_filter_by_date_of_birth(self):
        """
        Test filtering profiles by date of birth.
        """
        # Initialize the filter with the selected date of birth
        filter_set = self.filter_class(data={'date_of_birth': self.date_of_birth})
        # Assert that the filtered queryset contains profiles with the specified date of birth
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(date_of_birth=self.date_of_birth))
