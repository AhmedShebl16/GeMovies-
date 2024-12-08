from django.utils.timezone import now

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.compat import get_user_email, get_user_email_field_name

from .. import signals
from ..models import User
from ..utils import is_non_admin_user
from .filters import UserFilter


class UserViewSet(DjoserUserViewSet):
    """
    A ViewSet for viewing and editing user instances. Extends Djoser's UserViewSet
    and includes custom filtering and actions related to user management.
    """
    queryset = User.objects.exclude_admin()  # Custom queryset excluding admin users
    filterset_class = UserFilter  # Custom filter class for filtering user instances

    def get_queryset(self):
        """
        Retrieve the queryset for user instances. It modifies the default queryset
        to exclude the current user from the list view if they are a non-admin user.

        Returns:
            - QuerySet<User>: Modified queryset based on the user role and action.
        """
        # Get the default queryset from DjoserUserViewSet
        queryset = super(UserViewSet, self).get_queryset()
        # Get the current user
        user = self.request.user
        # Exclude the current non-admin user from the queryset if listing users
        if self.action == 'list' and is_non_admin_user(user):
            return queryset.exclude(id=user.id)
        return queryset

    def perform_destroy(self, instance):
        """
        Perform delete operation on a user instance. If settings allow, sends a
        deletion confirmation email before deleting the user.

        Args:
            - instance: The user instance to be deleted.
        """
        # Check if deletion confirmation is enabled in settings
        if getattr(settings, 'SEND_DELETE_CONFIRMATION', True):
            # Prepare email context and recipient
            context = {"user": instance}
            to = [get_user_email(instance)]
            # Send deletion confirmation email
            settings.EMAIL.delete(self.request, context).send(to)
        # Delete the user instance
        instance.delete()

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        """
        Handles user-specific requests based on the HTTP method used.

        This method provides a unified endpoint for various operations on the currently authenticated user.
        It supports GET for retrieving user details, PUT for updating user details, PATCH for partially updating
        user details, and DELETE for deleting the user account.

        The method dynamically sets the appropriate handler (retrieve, update, partial_update, destroy)
        based on the HTTP method specified in the request.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object, the nature of which depends on the HTTP method used in the request.
                      - GET returns user details.
                      - PUT and PATCH return the updated user details.
                      - DELETE returns a 204 No Content response on successful deletion.
        """
        return super().me(request, *args, **kwargs)

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        """
        Activates a user account.

        This method overrides the default activation behavior by setting the user's `is_active`
        attribute to True and then saving the user object. It also sends signals and confirmation
        emails if configured in the settings.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object with status code 204 (No Content) on successful activation.
       """
        return super().activation(request, *args, **kwargs)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        """
        Resends an activation email to a user who hasn't activated their account yet.

        This method handles POST requests to resend an activation email to users. It first validates
        the request data using a serializer and then checks if the user is eligible for receiving an
        activation email (i.e., they have not activated their account and the system is configured to
        send activation emails).

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object.
                      - Returns a 204 No Content response if the email is successfully sent.
                      - Returns a 400 Bad Request response if activation emails are not enabled or the user is not
                        found.
        """
        return super().resend_activation(request, *args, **kwargs)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        """
        Allows a user to set a new password for their account.

        This method handles POST requests for password change. It uses a serializer to validate
        the provided data, including the new password. Once validated, it sets the new password
        for the user making the request.

        After changing the password, it handles additional settings like sending a confirmation email
        if enabled, logging out the user on password change, or updating the session hash to keep
        the user logged in after password change based on the configuration settings.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object with a 204 No Content status, indicating successful password change.
        """
        return super().set_password(request, *args, **kwargs)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        """
        Initiates a password reset process for a user.

        This method handles POST requests to start the password reset process. It uses a serializer
        to validate the request data, primarily to identify the user who is requesting a password reset.
        If the user is found, the method sends a password reset email to the user's registered email address.

        The process of sending the email is managed by the configured email backend in the settings.
        This method ensures that the password reset email is sent, but the actual password reset process
        (i.e., setting a new password) is not handled here.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object with a 204 No Content status, indicating that the password reset
              request has been processed. Note that this does not necessarily mean the user's password has been  reset,
              only that the request has been acknowledged.
        """
        return super().reset_password(request, *args, **kwargs)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        """
        Confirms the password reset process by setting a new password for the user.

        This method handles POST requests to complete the password reset process. It validates the request data
        using a serializer, which includes the new password and any other necessary information to confirm the
        user's identity. Once validated, it sets the new password for the user and updates the user's last login
        time if applicable.

        If enabled in the settings, this method also sends a confirmation email to the user's email address to
        notify them of the successful password change.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object with a 204 No Content status, indicating that the password reset has
              been confirmed and the new password has been set successfully.
        """
        return super().reset_password_confirm(request, args, **kwargs)

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        """
        Custom action to set or change the username (or email if it is the username field) of the current user.
        Depending on the configuration, it may send confirmation emails and deactivate the user for reactivation.

        Args:
            - request: The HttpRequest object containing new username data.

        Returns:
            - Response: HTTP response with status indicating the outcome.
        """
        # Validate and deserialize input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get current user
        user = self.request.user
        # Extract and set the new username
        new_username = serializer.data["new_" + User.USERNAME_FIELD]
        setattr(user, User.USERNAME_FIELD, new_username)

        # Check if the username field is the email field
        email_field_name = get_user_email_field_name(user)
        if User.USERNAME_FIELD == email_field_name:
            # Deactivate user to re-activate through email confirmation
            user.is_active = False
            # Send user deactivated signal
            signals.user_deactivated.send(sender=self.__class__, user=user, request=self.request)
        # Save the updated user
        user.save()

        # Prepare context and recipient for confirmation emails
        context = {"user": user}
        to = [get_user_email(user)]
        # Send username changed confirmation email if setting is enabled
        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
        # Send activation email if setting is enabled and user is not active
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        """
        Initiates a username reset process for a user.

        This method handles POST requests to start the username reset process. It uses a serializer
        to validate the request data, primarily to identify the user who is requesting a username reset.
        If the user is found, the method sends a username reset email to the user's registered email address.

        The process of sending the email is managed by the configured email backend in the settings.
        This method ensures that the username reset email is sent, but the actual username reset process
        (i.e., setting a new username) is not handled here.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: An HTTP response object with a 204 No Content status, indicating that the username reset
              request has been processed. Note that this does not necessarily mean the user's username has been reset,
              only that the request has been acknowledged.
        """
        return super().reset_username(request, *args, **kwargs)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        """
        Custom action to confirm the username (or email) reset. It performs similar actions as set_username,
        confirming the username change and reactivating the user via email if needed.

        Args:
            - request: The HttpRequest object containing new username data.

        Returns:
            - Response: HTTP response with status indicating the outcome.
        """
        # Validate and deserialize input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Extract and set the new username
        new_username = serializer.data["new_" + User.USERNAME_FIELD]
        setattr(serializer.user, User.USERNAME_FIELD, new_username)
        # Update last_login if applicable
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()

        # Get the user from serializer
        user = serializer.user
        email_field_name = get_user_email_field_name(user)
        # Check if the username field is the email field
        if User.USERNAME_FIELD == email_field_name:
            # Deactivate user for re-activation
            user.is_active = False
            # Send user deactivated signal
            signals.user_deactivated.send(sender=self.__class__, user=user, request=self.request)
        # Save the updated user
        user.save()

        # Prepare context and recipient for confirmation emails
        context = {"user": user}
        to = [get_user_email(user)]
        # Send username changed confirmation email if setting is enabled
        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
        # Send activation email if setting is enabled and user is not active
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)
