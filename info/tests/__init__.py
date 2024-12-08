from accounts.tests import GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, FactoryTestCaseHelperMixin


class InfoTestCaseHelperMixin(GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, FactoryTestCaseHelperMixin):
    """
    A mixin to assist with information-related test cases.

    This mixin extends the functionalities of generic, model, and factory test case helper mixins to provide a focused
    environment for testing information-related models. It is tailored to handle models that might include fields such
    as 'image', timestamps like 'create_at' and 'update_at', or dates like 'join_date' and 'date', which are commonly
    excluded from direct comparison tests. Additionally, it ensures that the queryset only includes active instances
    if the model supports an 'is_active' field.
    """
    #: Default number of instances to generate for tests
    size = 10
    #: Fields to exclude in comparison tests
    exclude = ('image', 'create_at', 'update_at', 'join_date', 'date')

    def get_queryset(self, **kwargs):
        """
        Retrieves a queryset for the associated model, optionally filtering by provided keyword arguments.
        Automatically filters for active instances if the model has an 'is_active' field.

        Args:
            - **kwargs: Arbitrary keyword arguments used for filtering the queryset.

        Returns:
            - queryset (QuerySet): A Django queryset for the associated model, possibly filtered based on `kwargs`.
        """
        # Automatically include 'is_active=True' in the query if the model has an 'is_active' field
        if getattr(self.get_model(), 'is_active', None) is not None:
            kwargs.setdefault('is_active', True)
        return super().get_queryset(**kwargs)
