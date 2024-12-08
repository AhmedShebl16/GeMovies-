from typing import Callable

from rest_framework.permissions import BasePermission, SAFE_METHODS

from ..utils import is_customer_user, is_company_user, is_non_admin_user, is_owner


class ReadOnly(BasePermission):
    """
    Allows access only to safe methods: GET, HEAD, OPTIONS.
    This permission will be used to make a view or a method read-only.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the request method is a safe method.

        Args:
            - request: The HttpRequest object.
            - view: The view which is being accessed.

        Returns:
            - bool: True if the method is safe, False otherwise.
        """
        # Allow permission if the method is in the list of safe methods
        return request.method in SAFE_METHODS


class DenyDelete(BasePermission):
    """
    Denies access specifically to DELETE method.
    This permission can be used to prevent deleting resources in a view.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the request method is DELETE.

        Args:
            - request: The HttpRequest object.
            - view: The view which is being accessed.

        Returns:
            - bool: False if the method is DELETE, True otherwise.
        """
        # Deny permission if the method is DELETE
        return not request.method == 'DELETE'


class RoleBasePermissionMixin:
    """
    A mixin to provide role-based permissions in Django REST Framework views.
    It uses a user-defined function to determine the user's role and grants or denies
    permission based on that role.
    """

    # A callable that determines the user's role. Should be set or overridden in the subclass.
    user_role_function: Callable = None

    def get_user_role_function(self, request) -> Callable:
        """
        Retrieve the function used to determine the user's role.

        Args:
            - request: The HttpRequest object.

        Returns:
            - Callable: A function that takes a user and returns their role.
        """
        # Return the user_role_function set in the class.
        return self.user_role_function

    def has_permission(self, request, view) -> bool:
        """
        Determine if the request should be granted permission.

        Args:
            - request: The HttpRequest object.
            - view: The view which is being accessed.

        Returns:
            - bool: True if the request has permission, False otherwise.
        """
        user = request.user
        user_role_function = self.get_user_role_function(request)

        # Check if the user is authenticated and the user_role_function grants permission.
        has_perm = lambda args: user_role_function(args[1])
        return user.is_authenticated and has_perm

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Object level permission check.

        Args:
            - request: The HttpRequest object.
            - view: The view which is being accessed.
            - obj: The object being accessed.

        Returns:
            - bool: True if the request has permission for the specific object, False otherwise.
        """
        # Utilize a function to check if the user is the owner of the object.
        return is_owner(request.user, obj)


class IsCustomerUser(RoleBasePermissionMixin, BasePermission):
    """
    Permission class to check if a user is a customer. This class uses the
    RoleBasePermissionMixin to enforce that only users with a customer role
    are granted permission.
    """
    user_role_function: Callable = is_customer_user


class IsCompanyUser(RoleBasePermissionMixin, BasePermission):
    """
    Permission class to check if a user is associated with a company. This class uses
    the RoleBasePermissionMixin to enforce that only users with a company role
    are granted permission.
    """
    user_role_function: Callable = is_company_user


class IsNoneAdminUser(RoleBasePermissionMixin, BasePermission):
    """
    Permission class to check if a user is not an admin. This class uses the
    RoleBasePermissionMixin to enforce that users with any role other than
    admin are granted permission.
    """
    user_role_function: Callable = is_non_admin_user
