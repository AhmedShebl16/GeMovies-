from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from info.filters import (FAQsFilter, AboutUsFilter, TermsOfServiceFilter, CookiePolicyFilter, PrivacyPolicyFilter,
                          TeamMemberFilter, NewsFilter, AwardFilter, PartnerFilter)
from ..factories import (FAQsFactory, AboutUsFactory, TermsOfServiceFactory, CookiePolicyFactory, PrivacyPolicyFactory,
                         TeamMemberFactory, NewsFactory, AwardFactory, PartnerFactory)
from . import InfoTestCaseHelperMixin


class BaseInfoFilterTestCase(InfoTestCaseHelperMixin):
    """
    Base test case for testing filter functionalities on information-related models.

    This class tests basic filtering capabilities such as searching by title and description. It is designed to be
    extended by specific test cases for models that include title and description fields.
    """
    #: Number of instances to generate for each test scenario
    size = 5
    #: Default title used for generating test instances
    title = 'Title'
    #: Default description used for generating test instances
    description = 'Description'
    #: Placeholder for the specific filter class to be tested
    filter_class = None

    def setUp(self):
        """
        Set up the test environment by generating instances with specific titles and descriptions.
        """
        # Generate instances with a specific title
        self.generate_instances(size=self.size, title=self.title)
        # Generate instances with a specific description
        self.generate_instances(size=self.size, description=self.description)

    def test_search_filter_by_title(self):
        """
        Test that the filter correctly filters instances by part of the title.
        """
        # Apply the filter with a search term matching the title
        filter_set = self.filter_class(data={'search': self.title})
        # Assert that the filtered queryset contains only instances with the specified title
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(title__icontains=self.title))

    def test_search_filter_by_description(self):
        """
        Test that the filter correctly filters instances by part of the description.
        """
        # Apply the filter with a search term matching the description
        filter_set = self.filter_class(data={'search': self.description})
        # Assert that the filtered queryset contains only instances with the specified description
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(description__icontains=self.description))

    def test_filter_by_title(self):
        """
        Test that the filter correctly filters instances by the full title.
        """
        # Apply the filter with the full title
        filter_set = self.filter_class(data={'title': self.title})
        # Assert that the filtered queryset contains only instances with the exact title
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(title=self.title))

    def test_filter_by_description(self):
        """
        Test that the filter correctly filters instances by the full description.
        """
        # Apply the filter with the full description
        filter_set = self.filter_class(data={'description': self.description})
        # Assert that the filtered queryset contains only instances with the exact description
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(description=self.description))


class AboutUsFilterTestCase(BaseInfoFilterTestCase, TestCase):
    """
    Test case for filtering functionality on the About Us model.
    """
    #: Factory class for creating About Us instances
    factory_class = AboutUsFactory
    #: Filter class used for testing About Us model filtering
    filter_class = AboutUsFilter


class TermsOfServiceFilterTestCase(BaseInfoFilterTestCase, TestCase):
    """
    Test case for filtering functionality on the Terms Of Service model.
    """
    #: Factory class for creating Terms Of Service instances
    factory_class = TermsOfServiceFactory
    #: Filter class used for testing Terms Of Service model filtering
    filter_class = TermsOfServiceFilter


class CookiePolicyFilterTestCase(BaseInfoFilterTestCase, TestCase):
    """
    Test case for filtering functionality on the Cookie Policy model.
    """
    #: Factory class for creating Cookie Policy instances
    factory_class = CookiePolicyFactory
    #: Filter class used for testing Cookie Policy model filtering
    filter_class = CookiePolicyFilter


class PrivacyPolicyFilterTestCase(BaseInfoFilterTestCase, TestCase):
    """
    Test case for filtering functionality on the Privacy Policy model.
    """
    #: Factory class for creating Privacy Policy instances
    factory_class = PrivacyPolicyFactory
    #: Filter class used for testing Privacy Policy model filtering
    filter_class = PrivacyPolicyFilter


class FAQsFilterTestCase(InfoTestCaseHelperMixin, TestCase):
    """
    Test case for filtering functionality on the FAQs model.

    This class tests the filtering capabilities of the `FAQsFilter` class, ensuring that FAQs can be accurately
    filtered by attributes such as quote and answer. It leverages the FAQs factory methods to generate test FAQ
    instances with specific attributes for filtering.
    """
    #: Number of instances to generate for each test scenario
    size = 5
    #: Default quote used for generating test instances
    quote = 'Quote'
    #: Default answer used for generating test instances
    answer = 'Answer'
    #: Factory class for creating FAQ instances
    factory_class = FAQsFactory
    #: Filter class used for testing FAQs model filtering
    filter_class = FAQsFilter

    def setUp(self):
        """
        Set up the test environment by generating FAQ instances with specific quotes and answers.
        """
        # Generate instances with a specific quote
        self.generate_instances(size=self.size, quote=self.quote)
        # Generate instances with a specific answer
        self.generate_instances(size=self.size, answer=self.answer)

    def test_search_filter_by_quote(self):
        """
        Test that the filter correctly filters FAQs by part of the quote.
        """
        # Apply the filter with a search term matching the quote
        filter_set = self.filter_class(data={'search': self.quote})
        # Assert that the filtered queryset contains only instances with the specified quote
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(quote__icontains=self.quote))

    def test_search_filter_by_answer(self):
        """
        Test that the filter correctly filters FAQs by part of the answer.
        """
        # Apply the filter with a search term matching the answer
        filter_set = self.filter_class(data={'search': self.answer})
        # Assert that the filtered queryset contains only instances with the specified answer
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(answer__icontains=self.answer))

    def test_filter_by_quote(self):
        """
        Test that the filter correctly filters FAQs by the full quote.
        """
        # Apply the filter with the full quote
        filter_set = self.filter_class(data={'quote': self.quote})
        # Assert that the filtered queryset contains only instances with the exact quote
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(quote=self.quote))

    def test_filter_by_answer(self):
        """
        Test that the filter correctly filters FAQs by the full answer.
        """
        # Apply the filter with the full answer
        filter_set = self.filter_class(data={'answer': self.answer})
        # Assert that the filtered queryset contains only instances with the exact answer
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(answer=self.answer))


class TeamMemberFilterTestCase(InfoTestCaseHelperMixin, TestCase):
    """
    Test case for filtering functionality on the Team Member model.

    This class tests the filtering capabilities of the `TeamMemberFilter` class, ensuring that team members can be
    accurately filtered by attributes such as position, about text, active status, and join date. It leverages the
    Team Member factory methods to generate test instances with specific attributes for filtering.
    """
    #: Number of instances to generate for each test scenario
    size = 5
    #: Default 'about' text used for generating test instances
    about = 'About'
    #: Default 'position' used for generating test instances
    position = 'Position'
    #: Calculate a join date 2 years ago from today
    join_date = now().date() - timedelta(days=365*2)
    #: Factory class for creating Team Member instances
    factory_class = TeamMemberFactory
    #: Filter class used for testing Team Member model filtering
    filter_class = TeamMemberFilter

    def setUp(self):
        """
        Set up the test environment by generating Team Member instances with specific attributes.
        """
        # Generate instances with specific position, join date, and active status
        self.generate_instances(size=self.size, position=self.position, join_date=self.join_date, is_active=True)
        # Generate instances with specific 'about' text and active status
        self.generate_instances(size=self.size, about=self.about, is_active=True)

    def test_search_filter_by_position(self):
        """
        Test that the filter correctly filters Team Members by part of the position.
        """
        # Apply the filter with a search term matching the position
        filter_set = self.filter_class(data={'search': self.position})
        # Assert that the filtered queryset contains only instances with the specified position
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(position__icontains=self.position))

    def test_search_filter_by_about(self):
        """
        Test that the filter correctly filters Team Members by part of the 'about' text.
        """
        # Apply the filter with a search term matching the 'about' text
        filter_set = self.filter_class(data={'search': self.about})
        # Assert that the filtered queryset contains only instances with the specified 'about' text
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(about__icontains=self.about))

    def test_filter_by_is_active(self):
        """
        Test that the filter correctly filters Team Members by active status.
        """
        # Apply the filter with the 'is_active' status set to True
        filter_set = self.filter_class(data={'is_active': True})
        # Assert that the filtered queryset contains only active instances
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(is_active=True))

    def test_filter_by_join_date(self):
        """
        Test that the filter correctly filters Team Members by join date.
        """
        # Apply the filter with the specific join date
        filter_set = self.filter_class(data={'join_date': self.join_date})
        # Assert that the filtered queryset contains only instances with the specified join date
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(join_date=self.join_date))


class NewsFilterTestCase(BaseInfoFilterTestCase, TestCase):
    """
    Test case for filtering functionality on the News model.

    This class tests the filtering capabilities of the `NewsFilter` class, ensuring that news entries can be
    accurately filtered by attributes such as title, description, alt text, active status, and date. It extends
    the `BaseInfoFilterTestCase` to reuse the common filter tests and adds specific tests for news attributes.
    """
    #: Alternative text used for generating test news instances
    alt = 'Alt'
    #: Date used for generating test news instances, set to 2 days ago
    date = now().date() - timedelta(days=2)
    #: Factory class for creating News instances
    factory_class = NewsFactory
    #: Filter class used for testing News model filtering
    filter_class = NewsFilter

    def get_queryset(self, **kwargs):
        """
        Retrieves a queryset for the News model, optionally filtering by provided keyword arguments.

        Args:
            - **kwargs: Arbitrary keyword arguments used for filtering the queryset.

        Returns:
            - queryset (QuerySet): A Django queryset for the News model, filtered based on `kwargs`.
        """
        # Filter the queryset based on provided kwargs and ensure no duplicates by using distinct()
        return self.get_model().objects.filter(**kwargs).distinct()

    def setUp(self):
        """
        Set up the test environment by generating News instances with specific attributes.
        """
        # Generate instances with a specific title
        self.generate_instances(size=self.size, title=self.title)
        # Generate instances with a specific description
        self.generate_instances(size=self.size, description=self.description)
        # Generate instances with specific alt text and date
        self.generate_instances(size=self.size, alt=self.alt, date=self.date)

    def test_search_filter_by_alt(self):
        """
        Test that the filter correctly filters News entries by part of the alt text.
        """
        # Apply the filter with a search term matching the alt text
        filter_set = self.filter_class(data={'search': self.alt})
        # Assert that the filtered queryset contains instances with the specified alt text
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(**{'alt__icontains': self.alt}))

    def test_filter_by_alt(self):
        """
        Test that the filter correctly filters News entries by the full alt text.
        """
        # Apply the filter with the full alt text
        filter_set = self.filter_class(data={'alt': self.alt})
        # Assert that the filtered queryset contains only instances with the exact alt text
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(**{'alt': self.alt}))

    def test_filter_by_is_active(self):
        """
        Test that the filter correctly filters News entries by active status.
        """
        # Apply the filter with the 'is_active' status set to True
        filter_set = self.filter_class(data={'is_active': True})
        # Assert that the filtered queryset contains only active instances
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(**{'is_active': True}))

    def test_filter_by_date(self):
        """
        Test that the filter correctly filters News entries by date.
        """
        # Apply the filter with the specific date
        filter_set = self.filter_class(data={'date': self.date})
        # Assert that the filtered queryset contains only instances with the specified date
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(**{'date': self.date}))


class AwardFilterTestCase(InfoTestCaseHelperMixin, TestCase):
    """
    Test case for filtering functionality on the Award model.

    This class tests the filtering capabilities of the `AwardFilter` class, ensuring that awards can be accurately
    filtered by attributes such as name, description, organization, date, and active status. It leverages the Award
    factory methods to generate test instances with specific attributes for filtering.
    """
    #: Default name used for generating test award instances
    name = 'Name'
    #: Default description used for generating test award instances
    description = 'Description'
    #: Default organization associated with the award for generating test instances
    organization = 'Organization'
    #: Date associated with the award, set to 2 days ago from today
    date = now().date() - timedelta(days=2)
    #: Factory class for creating Award instances
    factory_class = AwardFactory
    #: Filter class used for testing Award model filtering
    filter_class = AwardFilter

    def setUp(self):
        """
        Set up the test environment by generating Award instances with specific attributes.
        """
        # Generate instances with a specific description
        self.generate_instances(size=self.size, description=self.description)
        # Generate instances with specific name and organization
        self.generate_instances(size=self.size, name=self.name, organization=self.organization)

    def test_search_filter_by_description(self):
        """
        Test that the filter correctly filters Awards by part of the description.
        """
        # Apply the filter with a search term matching the description
        filter_set = self.filter_class(data={'search': self.description})
        # Assert that the filtered queryset contains instances with the specified description
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(description__icontains=self.description))

    def test_search_filter_by_name(self):
        """
        Test that the filter correctly filters Awards by part of the name.
        """
        # Apply the filter with a search term matching the name
        filter_set = self.filter_class(data={'search': self.name})
        # Assert that the filtered queryset contains instances with the specified name
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(name__icontains=self.name))

    def test_search_filter_by_organization(self):
        """
        Test that the filter correctly filters Awards by part of the organization.
        """
        # Apply the filter with a search term matching the organization
        filter_set = self.filter_class(data={'search': self.organization})
        # Assert that the filtered queryset contains instances with the specified organization
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(organization__icontains=self.organization))

    def test_filter_by_date(self):
        """
        Test that the filter correctly filters Awards by date.
        """
        # Apply the filter with the specific date
        filter_set = self.filter_class(data={'date': self.date})
        # Assert that the filtered queryset contains only instances with the specified date
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(date=self.date))

    def test_filter_by_is_active(self):
        """
        Test that the filter correctly filters Awards by active status.
        """
        # Apply the filter with the 'is_active' status set to True
        filter_set = self.filter_class(data={'is_active': True})
        # Assert that the filtered queryset contains only active instances
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(is_active=True))


class PartnerFilterTestCase(InfoTestCaseHelperMixin, TestCase):
    """
    Test case for filtering functionality on the Partner model.

    This class tests the filtering capabilities of the `PartnerFilter` class, ensuring that partner entries can be
    accurately filtered by attributes such as name and description, and also by active status. It leverages the Partner
    factory methods to generate test instances with specific attributes for filtering.
    """
    #: Number of instances to generate for each test scenario
    size = 5
    #: Default name used for generating test partner instances
    name = 'Name'
    #: Default description used for generating test partner instances
    description = 'Description'
    #: Factory class for creating Partner instances
    factory_class = PartnerFactory
    #: Filter class used for testing Partner model filtering
    filter_class = PartnerFilter

    def setUp(self):
        """
        Set up the test environment by generating Partner instances with specific attributes.
        """
        # Generate instances with a specific description
        self.generate_instances(size=self.size, description=self.description)
        # Generate instances with a specific name
        self.generate_instances(size=self.size, name=self.name)

    def test_search_filter_by_description(self):
        """
        Test that the filter correctly filters Partners by part of the description.
        """
        # Apply the filter with a search term matching the description
        filter_set = self.filter_class(data={'search': self.description})
        # Assert that the filtered queryset contains instances with the specified description
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(**{'description__icontains': self.description}))

    def test_search_filter_by_name(self):
        """
        Test that the filter correctly filters Partners by part of the name.
        """
        # Apply the filter with a search term matching the name
        filter_set = self.filter_class(data={'search': self.name})
        # Assert that the filtered queryset contains instances with the specified name
        self.assertQuerysetContains(filter_set.qs, self.get_queryset(**{'name__icontains': self.name}))

    def test_filter_by_is_active(self):
        """
        Test that the filter correctly filters Partners by active status.
        """
        # Apply the filter with the 'is_active' status set to True
        filter_set = self.filter_class(data={'is_active': True})
        # Assert that the filtered queryset contains only active instances
        self.assertQuerysetEqual(filter_set.qs, self.get_queryset(**{'is_active': True}))
