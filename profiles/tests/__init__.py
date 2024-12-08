from accounts.tests import GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserTestCaseHelperMixin
from ..factories import ProfileFactory


class ProfileTestHelperMixin(GenericTestCaseHelperMixin, ModelTestCaseHelperMixin, UserTestCaseHelperMixin):
    """
    A mixin to assist with profile-related test cases.

    This mixin extends generic, model, and user test case helper mixins, specifically focusing on profile-related
    functionalities. It is designed to streamline the creation and management of profile instances in test cases,
    leveraging a ProfileFactory for consistent and efficient setup of test data.
    """
    #: Specifies the factory class used to create profile instances
    factory_class = ProfileFactory
