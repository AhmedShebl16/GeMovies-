from typing import Dict

from django.db import models

from rest_framework import serializers
from rest_framework.response import Response


class DynamicSerializerMixin:
    """
    Mixin to dynamically select a serializer class based on the current action.

    This mixin allows a view to use different serializers for different types of actions (e.g., 'list', 'create',
    'update', etc.) by mapping actions to serializer classes. It provides flexibility in how data is serialized
    and deserialized for different endpoints or request methods within a single view.

    Methods:
        - get_serializer_class: Determines and returns the appropriate serializer class for the current action.
    """

    #: A mapping of action names (as strings) to serializer classes (e.g., 'list', 'create').
    serializer_class_map: Dict[str, serializers.Serializer] = {}

    def get_serializer_class(self):
        """
        Determines the serializer class to use for the current action.

        This method checks if the current action has a corresponding serializer class defined in `serializer_class_map`.
         If so, it returns that class; otherwise, it defaults to the superclass's `get_serializer_class` method.

        Returns:
            The serializer class to be used for the current action.
        """
        serializer_class = self.serializer_class_map.get(self.action, None)
        if serializer_class is not None:
            return serializer_class
        return super().get_serializer_class()


class DynamicQuerysetMixin:
    """
    Mixin to dynamically select a queryset based on the current action.

    This mixin enhances a view by allowing it to define different querysets for different actions. It's useful for
    tailoring the set of objects returned or modified by the view, depending on the context of the request
    (e.g., different querysets for 'list' vs. 'detail' actions).

    Methods:
        - get_queryset: Retrieves and returns the appropriate queryset for the current action.
    """

    #: A mapping of action names (as strings) to queryset objects or classes.
    queryset_map: Dict[str, models.QuerySet] = {}

    def get_queryset(self):
        """
        Retrieves the queryset to use for the current action.

        This method checks if the current action has a corresponding queryset defined in `queryset_map`.
        If so, it returns that queryset; otherwise, it falls back to the predefined `queryset` attribute.

        Returns:
            The queryset to be used for the current action, ensuring it is always a fresh queryset instance by calling
            `.all()` if necessary.
        """
        queryset = self.queryset_map.get(self.action, self.queryset)
        if isinstance(queryset, models.QuerySet):
            queryset = queryset.all()
        return queryset


class ExtraContextListModelMixin:
    """
    Mixin to add extra context to list responses in DRF views.

    This mixin extends the list action of Django Rest Framework views to include additional context in the response.
    It works seamlessly with pagination, ensuring that extra context is included in paginated responses as well.
    To use it, simply include it in your view class and provide implementations for `set_paginated_context_data` and
    `get_paginated_response` methods, which are responsible for setting the extra context and returning the paginated
    response, respectively.
    """

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests and adds extra context to the list response.

        This method overrides the default list action to include additional context data in the response. It supports
        both paginated and non-paginated responses.

        Args:
            - request: The HTTP request object.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - Response: The list of serialized data, potentially paginated, and including any additional context.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # This method needs to be implemented in the subclass.
            self.set_paginated_context_data(**kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
