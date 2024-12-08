from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from drf_spectacular.utils import extend_schema
from rest_flex_fields.filter_backends import FlexFieldsDocsFilterBackend

from accounts.utils import is_customer_user
from accounts.api.permissions import IsCustomerUser
from ..models import Profile
from .filters import ProfileFilter
from .serializers import ProfileSerializer


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    """
    A viewset for viewing and editing user profiles. It provides endpoints for retrieving a single profile, updating
    profile details, and listing all profiles. It's intended for use by customers to manage their own profiles.
    """
    queryset = Profile.objects.active().with_age()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsAdminUser | IsCustomerUser]
    filter_backends = GenericViewSet.filter_backends + [FlexFieldsDocsFilterBackend]

    def get_permissions(self):
        """
        Determines the permissions for the current request based on the method and action.

        This method adjusts the permission classes based on the request method and specific action. For safe methods
        (e.g., GET), it ensures the user is authenticated. For the 'me' action, it sets the permission to check if the
        user is a customer.

        Returns:
            - permissions (list): A list of permission instances that should be applied to the request.

        Note:
            This method overrides a parent class's `get_permissions` method and should be used within a class that
            inherits from a view or viewset in Django REST framework.
        """
        # Check if the request method is considered "safe" (e.g., GET)
        if self.request.method in SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        # Check if the action is 'me' to apply customer-specific permissions
        elif self.action == 'me':
            permission_classes = [IsCustomerUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Retrieve the queryset for profile instances. It modifies the default queryset to exclude the current profile
        from the list view if they are a non-admin user.

        Returns:
            - QuerySet<User>: Modified queryset based on the user role and action.
        """
        queryset = super().get_queryset()
        # Get the current user
        user = self.request.user
        if self.action == 'list' and is_customer_user(user):
            return queryset.exclude(id=user.profile.id)
        return queryset

    def get_instance(self):
        """
        Retrieve the profile instance associated with the current user.

        Returns:
            - Profile: The profile instance of the current user.
        """
        return self.request.user.profile

    @extend_schema(responses={200: ProfileSerializer})
    @action(detail=False, methods=["GET", "PUT", "PATCH"], name='Get My Profile')
    def me(self, request, *args, **kwargs):
        """
        A custom action to retrieve or update the current user's profile. It supports GET for retrieving,
        PUT for full updates, and PATCH for partial updates.

        Args:
            - request: The HttpRequest object.

        Returns:
            - Response: The HTTP response with the profile data or update confirmation.
        """
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
