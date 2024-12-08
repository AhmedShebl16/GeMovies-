from django.test import TestCase
from django.urls import reverse, reverse_lazy

from rest_framework import status

from ..factories import (MainInfoFactory, FAQsFactory, AboutUsFactory, TermsOfServiceFactory, CookiePolicyFactory,
                         PrivacyPolicyFactory, ContactUsFactory, HeaderImageFactory, TeamMemberFactory, NewsFactory,
                         AwardFactory, PartnerFactory)
from . import InfoTestCaseHelperMixin


class MainInfoAPIViewTestCase(InfoTestCaseHelperMixin, TestCase):
    """
    Test case for the MainInfo API view.

    This class tests the API endpoint responsible for retrieving main information. It ensures the endpoint is
    accessible and returns the expected data structure.
    """
    #: Factory class for creating MainInfo instances
    factory_class = MainInfoFactory

    def setUp(self):
        """
        Set up the test environment before each test method.

        This method generates a MainInfo instance to be available for the API to retrieve.
        """
        # Generate a single MainInfo instance using the factory for testing
        self.generate_instance()

    def test_get_main_info(self):
        """
        Test retrieving the main information through the API.

        This method ensures that the API endpoint for fetching main information responds with a 200 OK status code and
        returns a non-empty data set.
        """
        # Define the URL for the 'main-info' endpoint using Django's `reverse` function
        url = reverse('info:main-info')

        # Make a GET request to the defined URL to test the API endpoint
        response = self.client.get(url)

        # Assert the response status code is 200 OK, indicating success
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data is not None, indicating that main information is returned
        self.assertIsNotNone(response.data)


class BaseInfoViewTestCase(InfoTestCaseHelperMixin):
    """
    Base test case for testing list view APIs for information-related models.

    This class provides a generic test for list views, ensuring that the API endpoint responds with the correct status
    code and data structure. It can be extended by specific view test cases to test various list view endpoints by
    simply specifying the URL and any model-specific configurations.
    """
    #: The API endpoint URL for the list view being tested.
    url: str

    def setUp(self):
        """
        Set up the test environment before each test method.

        This method generates a specified number of model instances to be available for the API to retrieve.
        """
        # Generate a specified number of instances using the factory for testing
        self.generate_instances(size=self.size)

    def test_get_model_list(self):
        """
        Test retrieving a list of model instances through the API.

        This method ensures that the API endpoint for fetching a list of model instances responds with a 200 OK status
        code and returns a data set that matches the number of generated instances.
        """
        # Make a GET request to the specified URL to test the API endpoint
        response = self.client.get(self.url)

        # Retrieve the queryset corresponding to the model instances
        queryset = self.get_queryset()

        # Assert the response status code is 200 OK, indicating success
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data includes a 'results' key
        self.assertIn('results', response.data)
        # Assert the number of items in 'results' matches the number of items in the queryset
        self.assertEqual(len(response.data['results']), queryset.count())
        # Assert that the items in 'results' match the items in the queryset, excluding specified fields
        self.assertQuerysetEqualList(queryset, response.data['results'], self.get_exclude())


class FAQsAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the FAQs API view.
    """
    #: Factory class for creating FAQ instances
    factory_class = FAQsFactory
    #: API endpoint URL for the FAQs list view
    url = reverse_lazy('info:fqa')


class AboutUsAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the About Us API view.
    """
    #: Factory class for creating About Us instances
    factory_class = AboutUsFactory
    #: API endpoint URL for the About Us list view
    url = reverse_lazy('info:about_us')


class TermsOfServiceAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Terms of Service API view.
    """
    #: Factory class for creating Terms of Service instances
    factory_class = TermsOfServiceFactory
    #: API endpoint URL for the Terms of Service list view
    url = reverse_lazy('info:terms_of_service')


class CookiePolicyAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Cookie Policy API view.
    """
    #: Factory class for creating Cookie Policy instances
    factory_class = CookiePolicyFactory
    #: API endpoint URL for the Cookie Policy list view
    url = reverse_lazy('info:cookie_policy')


class PrivacyPolicyAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Privacy Policy API view.
    """
    #: Factory class for creating Privacy Policy instances
    factory_class = PrivacyPolicyFactory
    #: API endpoint URL for the Privacy Policy list view
    url = reverse_lazy('info:privacy_policy')


class HeaderImageAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Header Image API view.
    """
    #: Factory class for creating Header Image instances
    factory_class = HeaderImageFactory
    #: API endpoint URL for the Header Images list view
    url = reverse_lazy('info:header_images')


class TeamMemberAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Team Members API view.
    """
    #: Factory class for creating Team Member instances
    factory_class = TeamMemberFactory
    #: API endpoint URL for the Team Members list view
    url = reverse_lazy('info:team_members')


class NewsAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the News API view.
    """
    #: Factory class for creating News instances
    factory_class = NewsFactory
    #: API endpoint URL for the News list view
    url = reverse_lazy('info:news')


class AwardAAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Awards API view.
    """
    #: Factory class for creating Award instances
    factory_class = AwardFactory
    #: API endpoint URL for the Awards list view
    url = reverse_lazy('info:awards')


class PartnerAPIViewTestCase(BaseInfoViewTestCase, TestCase):
    """
    Test case for the Partners API view.
    """
    #: Factory class for creating Partner instances
    factory_class = PartnerFactory
    #: API endpoint URL for the Partners list view
    url = reverse_lazy('info:partners')


class ContactUsAPIViewTestCase(InfoTestCaseHelperMixin, TestCase):
    """
    Test case for the ContactUs API view.

    This class tests the API endpoint responsible for creating new ContactUs entries. It ensures that the endpoint
    correctly creates entries with valid data and returns appropriate responses for invalid data.
    """
    #: Factory class for creating ContactUs instances
    factory_class = ContactUsFactory
    #: API endpoint URL for the ContactUs view
    url = reverse_lazy('info:contact_us')

    def test_create_contact_us(self):
        """
        Test creating a ContactUs entry with valid payload data.

        This method ensures that the API endpoint for creating a ContactUs entry responds with
        a 201 CREATED status code when provided with valid data.
        """
        # Generate a valid payload using instance data and adding a phone number
        valid_payload = self.instance_to_dict(self.generate_instance())
        valid_payload['phone_number'] = '+12495022991'

        # Make a POST request to the ContactUs API endpoint with the valid payload
        response = self.client.post(self.url, valid_payload, format='json')

        # Assert the response status code is 201 CREATED, indicating successful entry creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_contact_us_with_invalid_payload(self):
        """
        Test creating a ContactUs entry with invalid payload data.

        This method ensures that the API endpoint for creating a ContactUs entry responds with
        a 400 BAD REQUEST status code when provided with invalid data.
        """
        # Generate an invalid payload by intentionally providing an invalid email and a phone number
        invalid_payload = self.instance_to_dict(self.generate_instance(email='12345'))
        invalid_payload['phone_number'] = '+12495022991'

        # Make a POST request to the ContactUs API endpoint with the invalid payload
        response = self.client.post(self.url, invalid_payload, format='json')

        # Assert the response status code is 400 BAD REQUEST, indicating failure due to invalid data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
