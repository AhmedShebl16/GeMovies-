from rest_framework import serializers

from ..models import (MainInfo, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, FAQs, ContactUs, HeaderImage,
                      TeamMember, News, Award, Partner)


class MainInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for MainInfo model providing serialization and deserialization for all fields except explicitly excluded
    ones.
    """

    class Meta:
        model = MainInfo
        exclude = ()


class AboutUsSerializer(serializers.ModelSerializer):
    """
    Serializer for AboutUs model providing serialization and deserialization for all fields except explicitly excluded
    ones.
    """

    class Meta:
        model = AboutUs
        exclude = ()


class TermsOfServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for TermsOfService model providing serialization and deserialization for all fields except explicitly
    excluded ones.
    """

    class Meta:
        model = TermsOfService
        exclude = ()


class CookiePolicySerializer(serializers.ModelSerializer):
    """
    Serializer for CookiePolicy model providing serialization and deserialization for all fields except explicitly
    excluded ones.
    """

    class Meta:
        model = CookiePolicy
        exclude = ()


class PrivacyPolicySerializer(serializers.ModelSerializer):
    """
    Serializer for PrivacyPolicy model providing serialization and deserialization for all fields except explicitly
    excluded ones.
    """

    class Meta:
        model = PrivacyPolicy
        exclude = ()


class FAQsSerializer(serializers.ModelSerializer):
    """
    Serializer for FAQs model providing serialization and deserialization for all fields except explicitly excluded ones.
    """

    class Meta:
        model = FAQs
        exclude = ()


class ContactUsSerializer(serializers.ModelSerializer):
    """
    Serializer for ContactUs model providing serialization and deserialization for all fields except creation and
    update timestamps.
    """

    class Meta:
        model = ContactUs
        exclude = ('create_at', 'update_at')


class HeaderImageSerializer(serializers.ModelSerializer):
    """
    Serializer for HeaderImage model providing serialization and deserialization for all fields except explicitly
    excluded ones.
    """

    class Meta:
        model = HeaderImage
        exclude = ()


class TeamMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for TeamMember model providing serialization and deserialization for all fields except explicitly
    excluded ones. Includes a custom representation to handle image field specifically.
    """

    class Meta:
        model = TeamMember
        exclude = ()

    def to_representation(self, instance):
        """
        Custom to_representation method to handle image fields, setting default images if none provided.

        Args:
        - instance: The TeamMember instance being processed.

        Returns:
        - dict: The dictionary representation of the TeamMember instance with modified image handling.
        """
        data = super().to_representation(instance)

        request = self.context['request']

        # Set default image in case of being none
        if not instance.image:
            data['image'] = request.build_absolute_uri('/static/images/profile.png')

        return data


class NewsSerializer(serializers.ModelSerializer):
    """
    This serializer is used to convert News model instances into JSON format and vice versa. It is typically used in
    API endpoints to facilitate the creation, retrieval, updating, and deletion of news records through HTTP requests.
    """

    class Meta:
        model = News
        exclude = ()


class AwardSerializer(serializers.ModelSerializer):
    """
    This serializer handles the conversion of Award model instances to and from JSON format, enabling API interactions
    for award records. It is designed to support full CRUD (Create, Read, Update, Delete) operations via API requests.
    """

    class Meta:
        model = Award
        exclude = ()


class PartnerSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for converting instances of the Partner model into JSON format for API responses
    and parsing JSON data into Partner model instances for API requests. It supports comprehensive API functionalities
    for managing partner records.
    """

    class Meta:
        model = Partner
        exclude = ()
