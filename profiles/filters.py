from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AgeProfileListFilter(admin.SimpleListFilter):
    """
    Custom filter for Django admin to filter profiles based on age ranges. This filter will show up in the admin's list
    filter sidebar allowing admins to quickly filter out profiles falling into specific age groups.
    """
    title = _('Age')  # Human-readable title for the filter section.
    parameter_name = 'age'  # URL parameter name for the filter.

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples used to populate the filter options in the admin's sidebar.

        Args:
            - request: The HttpRequest object.
            - model_admin: The ModelAdmin instance for the queryset being filtered.

        Returns:
            - List[Tuple[str, str]]: A list of tuples where the first element is the coded value for the option that
              will appear in the URL query and the second element is the human-readable name for the option that will
              appear in the right sidebar.
        """
        return (
            ('0,18', _('Under Age')),
            ('18,30', _('In the twenties')),
            ('30,40', _('In the thirties')),
            ('40,50', _('In the forties')),
            ('50,60', _('In the fifties')),
            ('60,70', _('In the sixties')),
            ('70,80', _('In the seventies')),
            ('80,90', _('In the eighties')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the age range selected by the admin user.

        Args:
            - request: The HttpRequest object.
            - queryset: The original queryset that will be filtered.

        Returns:
            - QuerySet: The filtered queryset based on the selected age range.
        """
        # Get the selected age range value from the request's query string.
        val = self.value()
        # If no value is provided, don't alter the queryset.
        if val is None:
            return queryset
        # Split the provided value into start and end age.
        start_age, end_age = val.split(',')
        # Filter the queryset based on the age range and return it.
        return queryset.age_range(start_age, end_age)
