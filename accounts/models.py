from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from .enums import UserRoleChoices
from .validators import validate_boolean_true
from .constants import INVALID_TERMS_ERROR, INVALID_ROLE_ERROR


class CustomUserManager(UserManager):
    """
    Custom user manager that extends the default Django UserManager to provide role-based behaviors and additional
    queryset methods for user filtering.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a new user with the given username, email, and password.

        Args:
            - username: The username for the new user.
            - email: The email for the new user.
            - password: The password for the new user.
            - **extra_fields: Additional fields to include in the user creation.

        Raises:
            - ValueError: If role is not provided or is set as Admin for a normal user.

        Returns:
            - User: A new user object.
        """
        role = extra_fields.get('role', None)
        # Ensure for normal user that he doesn't have role admin or none
        if role is None:
            raise ValueError(_('Role can\'t be null'))
        elif role == UserRoleChoices.ADMIN:
            raise ValueError(_('Role can\'t be equal to Admin'))
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a new superuser with all permissions.

        Args:
            - username: The username for the new superuser.
            - email: The email for the new superuser.
            - password: The password for the new superuser.
            - **extra_fields: Additional fields to include in the superuser creation.

        Returns:
            - User: A new superuser object.
        """
        extra_fields.setdefault('role', UserRoleChoices.ADMIN)
        extra_fields.setdefault('terms_and_condition', True)
        return super().create_superuser(username, email, password, **extra_fields)

    def active(self, *args, **kwargs):
        """
        Return a queryset of active users.

        Returns:
            - QuerySet<User>: A queryset of users who are active.
        """
        return super().get_queryset(*args, **kwargs).filter(is_active=True)

    def exclude_admin(self, *args, **kwargs):
        """
        Return a queryset of active users excluding those with an admin role.

        Returns:
            - QuerySet<User>: A queryset of active users who are not admins.
        """
        return self.active().exclude(role=UserRoleChoices.ADMIN)


class User(AbstractUser):
    """
    User model that extends the default AbstractUser. This model adds additional fields and replaces the username field
    with an email field for authentication.
    """
    base_role = UserRoleChoices.OTHER

    email = models.EmailField(blank=False, unique=True, verbose_name=_('Email Address'))
    role = models.PositiveSmallIntegerField(choices=UserRoleChoices.choices, default=base_role, null=True,
                                            blank=True, verbose_name=_('Role'))
    terms_and_condition = models.BooleanField(default=True, blank=False, validators=[validate_boolean_true],
                                              verbose_name=_('Terms & condition'),
                                              help_text=_('Designates whether the user accept our terms and condition'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    # Set email as the unique identifier for auth instead of username
    USERNAME_FIELD = 'email'

    # Define additional required fields (besides email and password, which are default)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role', 'terms_and_condition']

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-date_joined', '-update_at')
        constraints = [
            # First CheckConstraint ensures that only superusers can have the 'ADMIN' role.
            models.CheckConstraint(
                name='superuser_must_be_admin',  # Human-readable name for the constraint.
                check=models.Q(is_superuser=True, role=UserRoleChoices.ADMIN) | models.Q(is_superuser=False),
                # The check uses a Q object to specify a condition: if a user is a superuser, then their role must be 'ADMIN'.
                # The '|' operator combines two conditions, meaning at least one must be true.
                # This allows non-superusers to have any role, but enforces superusers to have the 'ADMIN' role.
                violation_error_message=_(INVALID_ROLE_ERROR)
                # Custom error message for constraint violation (not supported in Django as of the last update).
            ),
            # Second CheckConstraint ensures that the 'terms_and_conditions' field is always True.
            models.CheckConstraint(
                name='terms_and_conditions_must_be_true',  # Human-readable name for the constraint.
                check=models.Q(terms_and_condition=True),
                # The check ensures the 'terms_and_conditions' field is True.
                violation_error_message=_(INVALID_TERMS_ERROR)
                # Custom error message for constraint violation (not supported in Django as of the last update).
            )
        ]

    def __str__(self):
        """
        String representation of the User model, typically used in the admin and during debugging.

        Returns:
            - str: An email address of the user.
        """
        return self.email
