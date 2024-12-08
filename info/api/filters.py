from django.db import models
from django_filters import rest_framework as filters

from ..models import FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, TeamMember, News, Award, Partner


class CustomSearchFilter(filters.FilterSet):
    """
    A custom filter set providing a basic search feature across title and description fields.
    """
    search = filters.CharFilter(method='custom_search', label="Search in title & description")

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the queryset based on the provided search value, searching across title and
        description fields.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset based on the search term.
        """
        return queryset.filter(models.Q(title__icontains=value) | models.Q(description__icontains=value))


class AboutUsFilter(CustomSearchFilter):
    """
    FilterSet for AboutUs model with custom search capabilities inherited from CustomSearchFilter.
    """

    class Meta:
        model = AboutUs
        fields = ('title', 'description', 'search')


class TermsOfServiceFilter(CustomSearchFilter):
    """
    FilterSet for TermsOfService model with custom search capabilities inherited from CustomSearchFilter.
    """

    class Meta:
        model = TermsOfService
        fields = ('title', 'description', 'search')


class CookiePolicyFilter(CustomSearchFilter):
    """
    FilterSet for CookiePolicy model with custom search capabilities inherited from CustomSearchFilter.
    """

    class Meta:
        model = CookiePolicy
        fields = ('title', 'description', 'search')


class PrivacyPolicyFilter(CustomSearchFilter):
    """
    FilterSet for PrivacyPolicy model with custom search capabilities inherited from CustomSearchFilter.
    """

    class Meta:
        model = PrivacyPolicy
        fields = ('title', 'description', 'search')


class FAQsFilter(filters.FilterSet):
    """
    A custom filter set specifically for the FAQs model, providing search features across quote and answer fields.
    """
    search = filters.CharFilter(method='custom_search', label="Search in quote & answer")

    class Meta:
        model = FAQs
        fields = ('quote', 'answer', 'search')

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the FAQs queryset based on the provided search value,
        searching across quote and answer fields.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset based on the search term.
        """
        return queryset.filter(models.Q(quote__icontains=value) | models.Q(answer__icontains=value))


class TeamMemberFilter(filters.FilterSet):
    """
    A custom filter set specifically for the TeamMember model, providing search features across position and about fields.
    """
    search = filters.CharFilter(method='custom_search', label="Search in position & about")

    class Meta:
        model = TeamMember
        fields = ('is_active', 'join_date', 'search')

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the TeamMember queryset based on the provided search value,
        searching across position and about fields.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset based on the search term.
        """
        return queryset.filter(models.Q(position__icontains=value) | models.Q(about__icontains=value))


class NewsFilter(filters.FilterSet):
    """
    A custom filter set specifically for the News model, providing search features different fields.
    """
    search = filters.CharFilter(method='custom_search', label="Search in title & description & alt")

    class Meta:
        model = News
        fields = ('date', 'is_active', 'title', 'description', 'alt', 'search')

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the News queryset based on the provided search value,
        searching across title & description & alt fields.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset based on the search term.
        """
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(alt__icontains=value)
        )


class AwardFilter(filters.FilterSet):
    """
    A custom filter set specifically for the Award model, providing search features different fields.
    """
    search = filters.CharFilter(method='custom_search', label="Search in name & organization & description")

    class Meta:
        model = Award
        fields = ('date', 'is_active', 'search')

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the Award queryset based on the provided search value,
        searching across title & description & alt fields.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset based on the search term.
        """
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(organization__icontains=value) |
            models.Q(description__icontains=value)
        )


class PartnerFilter(filters.FilterSet):
    """
    A custom filter set specifically for the Partner model, providing search features different fields.
    """
    search = filters.CharFilter(method='custom_search', label="Search in name & description")

    class Meta:
        model = Partner
        fields = ('is_active', 'search')

    def custom_search(self, queryset, name, value):
        """
        Custom search method to filter the News queryset based on the provided search value,
        searching across name & description fields.

        Args:
            - queryset: The original queryset to be filtered.
            - name: The name of the filter field, in this case, 'search'.
            - value: The value entered by the user to search for.

        Returns:
            - QuerySet: The filtered queryset based on the search term.
        """
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(description__icontains=value)
        )
