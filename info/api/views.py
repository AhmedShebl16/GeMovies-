from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView


from ..models import (MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, HeaderImage, TeamMember,
                      News, Award, Partner)
from .filters import (FAQsFilter, AboutUsFilter, TermsOfServiceFilter, CookiePolicyFilter, PrivacyPolicyFilter,
                      TeamMemberFilter, NewsFilter, AwardFilter, PartnerFilter)
from .serializers import (MainInfoSerializer, FAQsSerializer, AboutUsSerializer, TermsOfServiceSerializer,
                          CookiePolicySerializer, PrivacyPolicySerializer, ContactUsSerializer, HeaderImageSerializer,
                          TeamMemberSerializer, NewsSerializer, AwardSerializer, PartnerSerializer)


class MainInfoAPIView(RetrieveAPIView):
    """
    API view to retrieve the first MainInfo instance.
    """
    queryset = MainInfo.objects.all()
    serializer_class = MainInfoSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """
        Retrieve the first object from the queryset.

        Overrides the default get_object method to return the first instance from the queryset, instead of requiring
        lookup based on the pk or slug passed to the view. This is particularly useful for singleton models or when the
        view is meant to always display the first available instance, such as a main site configuration or information
        instance.

        Returns:
            - model instance: The first instance of the model from the queryset.
        """
        return self.get_queryset().first()


class FAQsAPIView(ListAPIView):
    """
    API view to list all FAQ instances.
    """
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    filterset_class = FAQsFilter
    permission_classes = [AllowAny]


class AboutUsAPIView(ListAPIView):
    """
    API view to list all AboutUs instances.
    """
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    filterset_class = AboutUsFilter
    permission_classes = [AllowAny]


class TermsOfServiceAPIView(ListAPIView):
    """
    API view to list all TermsOfService instances.
    """
    queryset = TermsOfService.objects.all()
    serializer_class = TermsOfServiceSerializer
    filterset_class = TermsOfServiceFilter
    permission_classes = [AllowAny]


class CookiePolicyAPIView(ListAPIView):
    """
    API view to list all CookiePolicy instances.
    """
    queryset = CookiePolicy.objects.all()
    serializer_class = CookiePolicySerializer
    filterset_class = CookiePolicyFilter
    permission_classes = [AllowAny]


class PrivacyPolicyAPIView(ListAPIView):
    """
    API view to list all PrivacyPolicy instances.
    """
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    filterset_class = PrivacyPolicyFilter
    permission_classes = [AllowAny]


class ContactUsAPIView(CreateAPIView):
    """
    API view to create a new ContactUs instance.
    """
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]


class HeaderImageAPIView(ListAPIView):
    """
    API view to list all active HeaderImage instances.
    """
    queryset = HeaderImage.objects.active()
    serializer_class = HeaderImageSerializer
    permission_classes = [AllowAny]


class TeamMemberAPIView(ListAPIView):
    """
    API view to list all active TeamMember instances.
    """
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    filterset_class = TeamMemberFilter
    permission_classes = [AllowAny]


class NewsAPIView(ListAPIView):
    """
    API view to list all active News instances.
    """
    queryset = News.objects.filter(is_active=True)
    serializer_class = NewsSerializer
    filterset_class = NewsFilter
    permission_classes = [AllowAny]


class AwardAPIView(ListAPIView):
    """
    API view to list all active Award instances.
    """
    queryset = Award.objects.filter(is_active=True)
    serializer_class = AwardSerializer
    filterset_class = AwardFilter
    permission_classes = [AllowAny]


class PartnerAPIView(ListAPIView):
    """
    API view to list all active Partner instances.
    """
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    filterset_class = PartnerFilter
    permission_classes = [AllowAny]
