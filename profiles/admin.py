from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from accounts.mixins import QuerysetAdminMixin
from .models import Profile
from .filters import AgeProfileListFilter


class ProfileAdmin(QuerysetAdminMixin, admin.ModelAdmin):
    """
    Admin interface option for Profile model with a custom queryset. It extends QuerysetAdminMixin to provide custom
    queryset filtering and admin.ModelAdmin for standard admin functionality.
    """
    queryset = Profile.objects.active().with_age()
    list_display = ('user', 'gender', 'create_at', 'update_at')
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__email']
    readonly_fields = ('create_at', 'update_at')
    list_filter = ('gender', AgeProfileListFilter, 'interest', 'reason')
    fieldsets = (
        (_('Personal info'), {'fields': ('user', 'gender', 'date_of_birth')}),
        (_('Contact Information'), {'fields': ('phone_number_1', 'phone_number_2')}),
        (_('Location'), {'fields': ('city', 'country', 'address')}),
        (_('Interest Details'), {'fields': ('interest', 'reason')}),
        (_('Important Dates'), {'fields': ('create_at', 'update_at')}),
    )
    list_per_page = 20
    date_hierarchy = 'create_at'


admin.site.register(Profile, ProfileAdmin)
