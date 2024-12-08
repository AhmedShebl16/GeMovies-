from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _, ngettext

from social_django.models import UserSocialAuth, Nonce, Association
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin class that extends Django's default UserAdmin.
    This class provides custom forms and actions for user model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'terms_and_condition',
                    'date_joined')
    actions = ['activate_users', 'deactivate_users']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'terms_and_condition', 'groups',
                       'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'terms_and_condition', 'password1',
                       'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'terms_and_condition', 'groups')
    list_per_page = 20
    date_hierarchy = 'date_joined'

    def get_form(self, request, obj=None, **kwargs):
        """
        Return a ModelForm for the given `obj` instance.

        Args:
            - request: The HttpRequest object.
            - obj: The object for which the form is being rendered.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - User: A ModelForm instance for the given object.
        """
        # Inherit the get_form method from the parent UserAdmin class
        form = super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
        # Iterate over fields that are both in form and required by user
        for field in filter(lambda field_name: field_name in User.REQUIRED_FIELDS, form.base_fields.keys()):
            # Set these fields as required
            form.base_fields[field].required = True
        return form

    def get_inlines(self, request, obj):
        """
        Determine the inlines for the `obj` detail view.

        Args:
            - request: The HttpRequest object.
            - obj: The object being viewed or edited.

        Returns:
            - list: A list of inline instances.
        """
        # Return no inlines for staff or superuser; otherwise, return class's inlines
        if not obj or (obj and (obj.is_staff or obj.is_superuser)):
            return []
        return self.inlines

    def deactivate_users(self, request, queryset):
        """
        Admin action to deactivate selected users.

        Args:
            - request: The HttpRequest object.
            - QuerySet[User]: The QuerySet of selected users to deactivate.
        """
        # Update is_active field to False for users who are currently active
        updated = queryset.filter(is_active=True).update(is_active=False)
        # Send success message to admin user interface
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user was successfully deactivated.",
                    "%d users were successfully deactivated.",
                    updated,
                ) % updated
            ),
            messages.SUCCESS,
        )

    # Description for the deactivate action
    deactivate_users.short_description = _('Deactivate selected Users')

    def activate_users(self, request, queryset):
        """
        Admin action to activate selected users.

        Args:
            - request: The HttpRequest object.
            - QuerySet[User]: The QuerySet of selected users to activate.
        """
        # Update is_active field to True for users who are currently inactive
        updated = queryset.filter(is_active=False).update(is_active=True)
        # Send success message to admin user interface
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user was successfully activated.",
                    "%d users were successfully activated.",
                    updated,
                ) % updated
            ),
            messages.SUCCESS,
        )

    # Description for the activate action
    activate_users.short_description = _('Activate selected Users')


admin.site.unregister(Nonce)
admin.site.unregister(Association)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
admin.site.register(User, CustomUserAdmin)
