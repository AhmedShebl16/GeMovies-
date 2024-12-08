from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite

from accounts.enums import UserRoleChoices
from ..admin import ProfileAdmin
from ..filters import AgeProfileListFilter
from . import ProfileTestHelperMixin


User = get_user_model()


class AgeProfileListFilterTestCase(ProfileTestHelperMixin, TestCase):
    """
    Test case for the age range filter in the profile admin.

    This class tests the custom age range filter functionality used in the Django admin to filter profiles
    by age. It ensures that the filter correctly identifies profiles within the specified age range.
    """

    @staticmethod
    def update_profile_date_of_birth_field(queryset, years):
        """
        Updates the 'date_of_birth' field for a given queryset of profiles to reflect the specified age.

        Args:
            queryset (QuerySet): The queryset of profiles to update.
            years (int): The age to set for these profiles, calculated backwards from today.
        """
        today = now().date()
        queryset.update(
            date_of_birth=today - timedelta(days=365 * years)
        )

    def setUp(self) -> None:
        """
        Set up the test environment by generating users with profiles and setting their ages.
        """
        self.size = 5
        # Generate users with a first name 'Jhon' and set their profile ages to 20 years
        self.generate_users(
            first_name='Jhon',
            size=self.size,
            is_active=True,
            role=UserRoleChoices.CUSTOMER,
        )
        # Generate users with a first name 'Micheal' and set their profile ages to 40 years
        self.generate_users(
            first_name='Micheal',
            size=self.size,
            is_active=True,
            role=UserRoleChoices.CUSTOMER,
        )

        # Update the 'date_of_birth' field for the profiles based on the specified ages
        self.update_profile_date_of_birth_field(
            self.get_model().objects.filter(user__first_name='Jhon'),
            20
        )
        self.update_profile_date_of_birth_field(
            self.get_model().objects.filter(user__first_name='Micheal'),
            40
        )

        # Initialize the ProfileAdmin instance to be used in the filter
        self.profile_admin = ProfileAdmin(self.get_model(), AdminSite())

    def test_admin_age_filter(self):
        """
        Test that the age range filter correctly filters profiles within the specified age range.
        """
        values = (18, 30)  # Define the age range for the filter
        # Initialize the age filter with the specified range
        age_filter = AgeProfileListFilter(None, {'age': ','.join(map(str, values))}, self.get_model(), self.profile_admin)
        # Apply the filter to the Profile queryset
        filtered_queryset = age_filter.queryset(None, self.get_model().objects.all())

        # Assert that the filtered queryset matches the expected queryset of profiles within the age range
        self.assertQuerysetEqual(self.get_model().objects.age_range(*values), filtered_queryset, ordered=False)
