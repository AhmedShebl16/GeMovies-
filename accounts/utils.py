from typing import Type

from django.db import models
from django.contrib.auth.backends import get_user_model

from profiles.models import Profile
from .enums import UserRoleChoices


User = get_user_model()


def _is_user_with_role(user: User, role: UserRoleChoices) -> bool:
    """
    Private helper function to check if a user has a specific role.

    Args:
        - user (User): The user whose role is to be checked.
        - role (UserRoleChoices): The role to check against the user's role.

    Returns:
        - bool: True if the user has the specified role, False otherwise.
    """
    return getattr(user, 'role', None) == role


def _is_instance_user(user: User, model: models.Model) -> bool:
    """
    Private helper function to check if a user is an instance of a specific model.

    Args:
        - user (User): The user to be checked.
        - model (models.Model): The Django model class to check against.

    Returns:
        - bool: True if the user is an instance of the specified model, False otherwise.
    """
    return isinstance(getattr(user, model.__name__.lower(), None), model)


def is_admin_user(user: User) -> bool:
    """
    Check if the user has an admin role.

    Args:
        - user (User): The user to be checked.

    Returns:
        - bool: True if the user is an admin, False otherwise.
    """
    return _is_user_with_role(user, UserRoleChoices.ADMIN)


def is_non_admin_user(user: User) -> bool:
    """
    Check if the user does not have an admin role.

    Args:
        - user (User): The user to be checked.

    Returns:
        - bool: True if the user is not an admin, False otherwise.
    """
    return not is_admin_user(user)


def is_customer_user(user: User) -> bool:
    """
    Check if the user has a customer role.

    Args:
        - user (User): The user to be checked.

    Returns:
        - bool: True if the user is a customer, False otherwise.
    """
    return _is_user_with_role(user, UserRoleChoices.CUSTOMER)


def is_company_user(user: User) -> bool:
    """
    Check if the user is associated with a company profile and has a company role.

    Args:
        - user (User): The user to be checked.

    Returns:
        - bool: True if the user is associated with a company and is a company user, False otherwise.
    """
    return _is_instance_user(user, Profile) and _is_user_with_role(user, UserRoleChoices.COMPANY)


def is_owner(user: User, obj: Type[models.Model]) -> bool:
    """
    Check if the user is the owner of the given object.

    Args:
        - user (User): The user to be checked.
        - obj (Type[models.Model]): The object to check ownership against.

    Returns:
        - bool: True if the user is the owner of the object, False otherwise.
    """
    if hasattr(obj, 'user'):
        if obj.user == user:
            return True
    if hasattr(obj, 'profile') and is_customer_user(user):
        if obj.profile == user.profile:
            return True
    return False
