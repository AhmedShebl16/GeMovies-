from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth.backends import get_user_model

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser

from drf_spectacular.utils import extend_schema

from profiles.models import Profile
from ..enums import ChartType
from .pagination import StatsPageNumberPagination
from .filters import UserStatsFilter, ProfileStatsFilter
from .mixins import DynamicSerializerMixin, DynamicQuerysetMixin, ExtraContextListModelMixin
from .serializers import (DateCountUserStatsSerializer, RoleCountUserStatsSerializer, DateCountProfileStatsSerializer,
                          InterestCountProfileStatsSerializer, ReasonCountProfileStatsSerializer)


User = get_user_model()


class BaseStatsGenericViewSet(DynamicQuerysetMixin, DynamicSerializerMixin, GenericViewSet):
    """
    Base viewset for statistics-related APIs.

    Incorporates dynamic querying and serialization capabilities, tailored for handling statistical data. It ensures
    that only admin users have access to the viewset and employs a custom pagination strategy to optimize data
    presentation. Additionally, it supports injecting extra context into the paginated responses, enhancing the
    flexibility and usefulness of the API responses.
    """

    #: Defines the permissions required to access this viewset. Set to `IsAdminUser` to restrict access to admin users only.
    permission_classes = [IsAdminUser]
    #: Specifies the pagination scheme used for list responses, tailored for statistical data.
    pagination_class = StatsPageNumberPagination
    #: Points to the `list` method from `ListModelMixin`, enabling the listing of queryset ITEMS.
    list_view = ExtraContextListModelMixin.list
    #: Stores additional context data to be included in paginated responses.
    extra_context = None

    def get_paginated_context_data(self, **kwargs):
        """
        Retrieves additional context data for inclusion in paginated responses.

        This method merges any predefined extra context data with the provided keyword arguments, allowing for dynamic
        context data extension.

        Args:
            - **kwargs: Arbitrary keyword arguments that may contain additional context data.

        Returns:
            - dict: A dictionary containing the combined extra context data.
        """
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def set_paginated_context_data(self, **kwargs):
        """
        Sets additional context data for the paginator.

        This method allows for the dynamic setting of context data to be included in paginated responses, utilizing
        the paginator's `set_context_data` method.

        Args:
            - **kwargs: Arbitrary keyword arguments that may contain additional context data.
        """
        self.paginator.set_context_data(**self.get_paginated_context_data(**kwargs))


class UserStatsViewSet(BaseStatsGenericViewSet):
    """
    Viewset for user statistics.

    This viewset extends `BaseStatsGenericViewSet` to provide specific endpoints for user statistics, such as daily
    user registration counts and counts by user role. It uses custom querysets and serializers for each statistical
    endpoint to tailor the data presentation.
    """

    #: The base queryset for user statistics, excluding admin users.
    queryset = User.objects.exclude_admin()
    #: The filter class used to filter the queryset based on provided query parameters.
    filterset_class = UserStatsFilter
    #: A mapping from action names to serializers. This allows different serializers to be used for different actions.
    serializer_class_map = {
        'daily_count': DateCountUserStatsSerializer,
        'role_count': RoleCountUserStatsSerializer
    }
    #: A mapping from action names to querysets. This allows custom querysets to be used for different actions.
    queryset_map = {
        'daily_count': queryset.annotate(
                date=TruncDate('date_joined')
            ).values(
                'date'
            ).annotate(
                count=Count('id')
            ).order_by(
                '-date'
            ),
        'role_count': queryset.values(
                'role'
            ).annotate(
                count=Count('id')
            ).order_by(
                'count'
            )
    }

    @extend_schema(responses={200: DateCountUserStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        """
        Endpoint for daily user registration counts.

        Args:
            - request (HttpRequest): The request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: The list view response containing daily user registration counts.
        """
        self.extra_context = {'chart': ChartType.LINE}
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: RoleCountUserStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='role-count')
    def role_count(self, request, *args, **kwargs):
        """
        Endpoint for user counts by role.

        Args:
            - request (HttpRequest): The request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: The list view response containing counts of users by their roles.
        """
        self.extra_context = {'chart': ChartType.PIE}
        return self.list_view(request, *args, **kwargs)


class ProfileStatsViewSet(BaseStatsGenericViewSet):
    """
    Viewset for profile statistics.

    This viewset extends `BaseStatsGenericViewSet` to provide specific endpoints for profile statistics, such as daily
    profile creation counts, counts by interest, and counts by reason for profile creation. It customizes the base
    queryset, filter class, and serializer class map for these specific statistical views.
    """

    #: The base queryset for profile statistics, including all profiles.
    queryset = Profile.objects.all()
    #: The filter class used to filter the queryset based on provided query parameters.
    filterset_class = ProfileStatsFilter
    #: A mapping from action names to serializers. This allows different serializers to be used for different actions.
    serializer_class_map = {
        'daily_count': DateCountProfileStatsSerializer,
        'interest_count': InterestCountProfileStatsSerializer,
        'reason_count': ReasonCountProfileStatsSerializer
    }
    #: A mapping from action names to querysets. This allows custom querysets to be used for different actions.
    queryset_map = {
        'daily_count': queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('-date'),
        'interest_count': queryset.values('interest').annotate(
                count=Count('id')
            ).order_by('count'),
        'reason_count': queryset.values('reason').annotate(
                count=Count('id')
            ).order_by('count')
    }

    @extend_schema(responses={200: DateCountProfileStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        """
        Endpoint for daily profile creation counts.

        Args:
            - request (HttpRequest): The request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: The list view response containing daily profile creation counts.
        """
        self.extra_context = {'chart': ChartType.LINE}
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: DateCountProfileStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='interest-count')
    def interest_count(self, request, *args, **kwargs):
        """
        Endpoint for profile counts by interest.

        Args:
            - request (HttpRequest): The request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: The list view response containing counts of profiles by their interest.
        """
        self.extra_context = {'chart': ChartType.PIE}
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: DateCountProfileStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='reason-count')
    def reason_count(self, request, *args, **kwargs):
        """
        Endpoint for profile counts by creation reason.

        Args:
            - request (HttpRequest): The request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: The list view response containing counts of profiles by their reason for creation.
        """
        self.extra_context = {'chart': ChartType.PIE}
        return self.list_view(request, *args, **kwargs)
