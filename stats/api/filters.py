from django_filters import rest_framework as filters

from accounts.models import User
from accounts.enums import UserRoleChoices
from profiles.models import Profile


class UserStatsFilter(filters.FilterSet):
    """
    Filter for User statistics.

    This class is designed to filter User model instances based on their role and the day of their
    date_joined attribute. It's particularly useful for narrowing down users with specific roles and
    joining dates, allowing for a more targeted selection in queries. The class leverages Django's
    FilterSet capabilities to provide customizable filtering options.

    Note:
        The `date_joined` filters compare against the 'day' part of the `date_joined` datetime field.
    """

    role = filters.ChoiceFilter(choices=UserRoleChoices.non_admin_choices)
    date_joined = filters.NumberFilter(field_name='date_joined', lookup_expr='day')
    date_joined_day__gt = filters.NumberFilter(field_name='date_joined', lookup_expr='day__gt')
    date_joined_day__lt = filters.NumberFilter(field_name='date_joined', lookup_expr='day__lt')

    class Meta:
        model = User
        fields = ('date_joined', 'role')


class BaseCreateAtStatsFilter(filters.FilterSet):
    """
    Base filter for objects based on their creation date.

    This class provides a foundational filtering mechanism for any model that includes a 'create_at'
    datetime field. It enables filtering of objects by the day part of their creation date, including
    options to filter for objects created on, before, or after a specific day.

    Note:
        The filters operate on the 'day' part of the `create_at` datetime field, allowing for day-level granularity in
        filtering.
    """

    create_at = filters.NumberFilter(field_name='create_at', lookup_expr='day')
    create_at_day__gt = filters.NumberFilter(field_name='create_at', lookup_expr='day__gt')
    create_at_day__lt = filters.NumberFilter(field_name='create_at', lookup_expr='day__lt')

    class Meta:
        fields = ('create_at',)


class ProfileStatsFilter(BaseCreateAtStatsFilter):
    """
    Filter for Profile statistics extending the BaseCreateAtStatsFilter.

    This class expands upon the BaseCreateAtStatsFilter by specifically targeting the Profile model.
    It allows for filtering of Profile instances not only based on their creation date (inherited functionality)
    but also on various profile-specific fields such as gender, date of birth, city, country, address, interest,
    and reason for joining. It's tailored to facilitate detailed querying of Profile records based on a broad
    range of attributes.

    Note:
        Inherits 'create_at', 'create_at_day__gt', and 'create_at_day__lt' filters from BaseCreateAtStatsFilter,
        allowing for filtering by the creation date of the Profile instances.
    """

    class Meta:
        model = Profile
        fields = ('gender', 'date_of_birth', 'city', 'country', 'address', 'interest', 'reason')
