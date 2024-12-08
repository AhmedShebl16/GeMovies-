from accounts.tests import GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserTestCaseHelperMixin


class StatsTestCaseHelperMixin(GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserTestCaseHelperMixin):
    """
    A mixin to assist with statistics-related test cases.

    This mixin is designed to provide common setup and utilities for test cases that involve statistical analyses or
    calculations. It extends the generic, model, and user test case helper mixins to offer a comprehensive testing
    environment tailored for statistics-related functionalities.
    """
    #: Default number of instances to generate in test cases, can be overridden as needed
    size = 5
