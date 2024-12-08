from django.test import TestCase

from ..factories import (MainInfoFactory, FAQsFactory, AboutUsFactory, TermsOfServiceFactory, CookiePolicyFactory,
                         PrivacyPolicyFactory, ContactUsFactory, HeaderImageFactory, TeamMemberFactory, NewsFactory,
                         AwardFactory, PartnerFactory)
from . import InfoTestCaseHelperMixin


class BaseInfoModelTestCase(InfoTestCaseHelperMixin):
    """
    Base test case for testing basic model functionalities for information-related models.

    This class is designed to test the creation of model instances and their string representation. It serves as a
    foundation for more specific model test cases, ensuring that model instances can be created with all required
    fields and their string representation is as expected.
    """
    #: Specifies the field name used in the model's __str__ method
    str_repr_field: str

    def setUp(self):
        """
        Set up the test environment by generating model instances.
        """
        # Generate model instances using the factory class defined in the mixin
        self.generate_instances(size=self.size)

    def get_instance_repr(self, instance):
        """
        Retrieve the string representation of a model instance based on `str_repr_field`.

        Args:
            - instance: The model instance from which to retrieve the string representation.

        Returns:
            - Any: The string representation of the instance as defined by `str_repr_field`.
        """
        # Get the attribute specified by `str_repr_field` from the instance, if it exists
        return getattr(instance, self.str_repr_field, None)

    def test_create_model_instance(self):
        """
        Test the creation of model instances and their string representation.
        """
        # Retrieve all created instances using the defined queryset
        queryset = self.get_queryset()

        # Iterate over each instance in the queryset
        for instance in queryset:
            # Assert that all fields except those in `exclude` are not None
            self.assertModelFieldsNotNone(instance, self.get_exclude())
            # Assert that the string representation of the instance matches the expected value
            self.assertEqual(str(instance), self.get_instance_repr(instance))


class MainInfoModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the MainInfo model to ensure the model instance is created properly and has the correct string
    representation based on the 'email' field.
    """
    #: Number of instances to generate for each test scenario
    size = 1
    #: Factory class for creating MainInfo instances
    factory_class = MainInfoFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'email'


class FAQsModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the FAQs model to ensure the model instance is created properly and has the correct string
    representation based on the 'quote' field.
    """
    #: Factory class for creating FAQs instances
    factory_class = FAQsFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'quote'


class AboutUsModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the AboutUs model to ensure the model instance is created properly and has the correct string
    representation based on the 'title' field.
    """
    #: Factory class for creating AboutUs instances
    factory_class = AboutUsFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'title'


class TermsOfServiceModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the TermsOfService model to ensure the model instance is created properly and has the correct string
    representation based on the 'title' field.
    """
    #: Factory class for creating TermsOfService instances
    factory_class = TermsOfServiceFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'title'


class CookiePolicyModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the CookiePolicy model to ensure the model instance is created properly and has the correct string
    representation based on the 'title' field.
    """
    #: Factory class for creating CookiePolicy instances
    factory_class = CookiePolicyFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'title'


class PrivacyPolicyModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the PrivacyPolicy model to ensure the model instance is created properly and has the correct string
    representation based on the 'title' field.
    """
    #: Factory class for creating PrivacyPolicy instances
    factory_class = PrivacyPolicyFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'title'


class TeamMemberModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the TeamMember model to ensure the model instance is created properly and has the correct string
    representation based on the 'name' field.
    """
    #: Factory class for creating TeamMember instances
    factory_class = TeamMemberFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'name'


class NewsModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the News model to ensure the model instance is created properly and has the correct string
    representation based on the 'title' field.
    """
    #: Factory class for creating News instances
    factory_class = NewsFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'title'


class AwardModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the Award model to ensure the model instance is created properly and has the correct string
    representation based on the 'name' field.
    """
    #: Factory class for creating Award instances
    factory_class = AwardFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'name'


class PartnerModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the Partner model to ensure the model instance is created properly and has the correct string
    representation based on the 'name' field.
    """
    #: Factory class for creating Partner instances
    factory_class = PartnerFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'name'


class HeaderImageModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the HeaderImage model to ensure the model instance is created properly and has the correct string
    representation based on the 'title' field.
    """
    #: Factory class for creating HeaderImage instances
    factory_class = HeaderImageFactory
    #: Specifies the field name used in the model's __str__ method
    str_repr_field = 'title'


class ContactUsModelTestCase(BaseInfoModelTestCase, TestCase):
    """
    Test case for the ContactUs model to ensure the model instance is created properly and has the correct string
    representation based on the 'first_name' and 'last_name' fields.
    """
    #: Factory class for creating ContactUs instances
    factory_class = ContactUsFactory

    def get_instance_repr(self, instance):
        """
        Retrieve the string representation of a ContactUs model instance, formatted as 'first_name last_name'.

        Args:
            - instance: The ContactUs model instance from which to retrieve the string representation.

        Returns:
            - str: The string representation of the instance, formatted as 'first_name last_name'.
        """
        # Get the 'first_name' and 'last_name' attributes from the instance
        first_name = getattr(instance, 'first_name', None)
        last_name = getattr(instance, 'last_name', None)
        # Format and return the string representation as 'first_name last_name'
        return f'{first_name} {last_name}'
