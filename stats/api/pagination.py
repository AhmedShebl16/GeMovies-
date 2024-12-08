from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StatsPageNumberPagination(PageNumberPagination):
    """
    Custom pagination for statistics pages.

    This class extends the PageNumberPagination to provide customized pagination functionality specifically for
    statistics pages. It allows clients to control the number of items per page and caps the maximum number of items
    per page to prevent overloading the server. Additionally, it supports adding extra context to the paginated
    response,making it more flexible for various use cases.
    """

    #: The default number of items to include on each page if not specified by the client in the  request.
    page_size: int = 50
    #: The name of the query parameter to specify the number of items they want to include on each page.
    page_size_query_param: str = 'page_size'
    #: The maximum allowable number of items on each page, providing an upper limit for the `page_size_query_param`
    max_page_size: int = 100
    #: Additional context data to be included in the paginated response.
    context = None

    def set_context_data(self, **kwargs) -> None:
        """
        Sets the additional context data for the paginated response.

        Args:
            - **kwargs: Arbitrary keyword arguments containing context data.
        """
        self.context = kwargs

    def get_context_data(self):
        """
        Retrieves the additional context data for the paginated response.

        Returns:
            - dict: The context data set by `set_context_data`.
        """
        return self.context

    def get_paginated_response(self, data: list) -> Response:
        """
        Constructs the paginated response with additional context data.

        Args:
            - data (list): The data items to include in the current page of the response.

        Returns:
            - Response: An OrderedDict containing pagination details and the data for the current page, along with any
              additional context data.
        """
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('extra', self.get_context_data()),
            ('results', data)
        ]))
