from typing import List

from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS


class SafeMethodsOrCustomPermissionViewMixin:
    """
    Mixin to allow safe methods (GET, HEAD, OPTIONS) for any user, while applying permission classes for other methods.
    This is particularly useful in API views where you want to allow read-only access broadly, but restrict write or
    other unsafe operations to certain users.
    """
    save_methods: List[str] = SAFE_METHODS
    save_methods_permission_classes: List[BasePermission] = [AllowAny]

    def get_permission_classes(self, request):
        """
        Determine the permission classes to apply based on the request method.

        Args:
            - request: The HttpRequest object.

        Returns:
            - list: The appropriate permission classes for the request method.
        """
        # Check if the request method is considered safe
        if request.method in self.save_methods:
            # Return the safe methods' permission classes
            return self.save_methods_permission_classes
        # For other methods, return the default permission classes from the parent class
        return super().get_permission_classes(request)
