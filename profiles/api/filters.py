from django.db import models

from django_filters import rest_framework as filters

from ..models import Profile


class ProfileFilter(filters.FilterSet):
    """
    Filter set for the Profile model to filter by various attributes such as gender,
    date of birth, interest, and reason, and also allow for a custom search across
    user's first and last names, email, and username.
    """
    # Define a character filter for searching across user's first and last names, email, and username
    search = filters.CharFilter(method='custom_search', label="Search first & last names, email, and username")

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the queryset based on the search value
        across user's first name, last name, email, and username.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset.
        """
        # Filter the queryset based on a case-insensitive containment check across specified user fields
        return queryset.filter(
            models.Q(user__first_name__icontains=value) | models.Q(user__last_name__icontains=value) |
            models.Q(user__email__icontains=value) | models.Q(user__username__icontains=value)
        )

    class Meta:
        model = Profile  # Define which model this filter set is for
        fields = ('gender', 'date_of_birth', 'interest', 'reason', 'search')  # Define the fields that can be filtered
