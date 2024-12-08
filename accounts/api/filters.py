from django.db import models

from django_filters import rest_framework as filters

from ..models import User
from ..enums import UserRoleChoices


class UserFilter(filters.FilterSet):
    """
    A filter set for the User model to filter by various user attributes such
    as name, username, email, and role. It's intended for use with Django's
    filtering backend in a REST framework view.
    """
    # Define a character filter for searching across first name, last name, username, and email
    search = filters.CharFilter(method='custom_search', label="Search first & last name, username and email")
    # Define a choice filter for user roles, excluding admin choices
    role = filters.ChoiceFilter(choices=UserRoleChoices.non_admin_choices)

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the queryset based on the search value
        across first name, last name, username, and email.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet<User>: The filtered queryset.
        """
        # Filter the queryset for any user where the search value is in their first name, last name,
        # username, or email, using case-insensitive containment checks.
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value) |
            models.Q(email__icontains=value) | models.Q(username__icontains=value)
        )

    class Meta:
        model = User  # Define which model this filter set is for
        fields = ('search', 'role')  # Define the fields that can be filtered
