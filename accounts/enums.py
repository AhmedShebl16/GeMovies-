from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class classproperty(property):
    """
    A decorator to define a class-level property that can be accessed directly from the class without requiring an
    instance.
    It allows a class method to be accessed as a class property.
    """

    def __get__(self, owner_self, owner_cls):
        # If accessed through an instance, owner_self will be set; otherwise, it's accessed through the class.
        return self.fget(owner_cls)  # Call the function with the class (owner_cls) as its argument.


class UserRoleChoices(models.IntegerChoices):
    """
    Enumeration for user role choices using Django's IntegerChoices for storing user roles.
    """
    # Define the choices as constants
    ADMIN = 0, _('Admin')
    CUSTOMER = 1, _('Customer')
    COMPANY = 2, _('Company')
    OTHER = 3, _('Other')

    @classmethod
    def excluded(cls, exclude: List = None):
        """
        Returns choices excluding the specified values.

        Args:
            - exclude: A list of values to exclude from the choices.

        Returns:
            - List[UserRoleChoices]: A list of tuples representing the remaining choices.
        """
        exclude = exclude or []  # Default to an empty list if none provided
        # Filter out the excluded choices and return the rest
        return [(label, value) for label, value in cls.choices if value not in exclude]

    @classproperty
    def non_admin_choices(cls):
        """
        Returns all choices except the ADMIN.

        Returns:
            - List<UserRoleChoices>: A list of tuples representing all non-admin choices.
        """
        # Utilize the excluded method to filter out the ADMIN choice
        return cls.excluded([cls.ADMIN.value])
