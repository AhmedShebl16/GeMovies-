

class QuerysetAdminMixin:
    """
    A mixin for Django admin classes to customize the queryset used in the admin view.
    It allows specifying a custom queryset or uses the default manager's queryset.
    """
    queryset = None

    def get_queryset(self, request):
        """
        Returns the queryset to be used in the admin view for the model.

        Args:
            - request: The HttpRequest object.

        Returns:
            - QuerySet[Model]: A queryset that will be used to display the model's list in the admin.
        """
        # Check if a custom queryset has been specified
        if self.queryset is None:
            # If not, use the default manager's queryset
            qs = self.model._default_manager.get_queryset()
        else:
            # Use the custom queryset if it's specified
            qs = self.queryset
        # Get the ordering specified for the admin view
        ordering = self.get_ordering(request)
        if ordering:
            # Apply the ordering to the queryset if any ordering is specified
            qs = qs.order_by(*ordering)
        return qs
