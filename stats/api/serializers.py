from django.contrib.auth.backends import get_user_model

from rest_framework import serializers

from accounts.enums import UserRoleChoices
from profiles.models import Profile
from profiles.enums import GenderChoices, InterestChoices, ReasonChoices


User = get_user_model()


class CustomChoiceCharField(serializers.CharField):
    """
    Custom field for handling choice-based fields in serializers.

    This class extends the CharField from serializers to provide a way to handle enumeration-like choice fields. It
    allows the serialization and deserialization of enum-like objects where each choice is represented by a value and a
    corresponding human-readable label. It ensures that the API can work with the readable labels while still using the
    actual enum values internally.
    """

    def __init__(self, choices, **kwargs):
        """
        Initializes the custom choice char field with the given choices.

        Args:
            - choices (Enum): An enumeration-like object containing the available choices.
            - **kwargs: Additional keyword arguments passed to the CharField constructor.
        """
        super().__init__(**kwargs)
        self.choices = choices

    def to_representation(self, value):
        """
        Converts the enum value to its readable string representation.

        Args:
            - value: The enum value to be converted.

        Returns:
            - str: The readable string representation of the enum value.
        """
        choice = self.choices(value)
        return choice.label

    def to_internal_value(self, data):
        """
        Converts the input data to the corresponding enum value.

        Args:
            - data (str): The input data corresponding to the choice's readable label.

        Returns:
            - Any: The enum value corresponding to the input data's label.

        Raises:
            - serializers.ValidationError: If the input data does not match any choice label.
        """
        for choice in self.choices:
            if data == choice.label:
                return choice.value
        raise serializers.ValidationError(f"{data} is not a valid choice.")


class BaseDateCountStatsSerializer(serializers.ModelSerializer):
    """
    Base serializer for statistics with date and count.

    This serializer provides a generic structure for statistics that involve a date and a count, such as daily user
    registrations or daily profile creations. It is intended to be extended by more specific serializers that associate
    the structure with a particular model.
    """

    #: Field for representing the date associated with the count.
    date = serializers.DateField()
    #: Field for representing the count on the specified date.
    count = serializers.IntegerField()

    class Meta:
        fields = ('date', 'count')


class DateCountUserStatsSerializer(BaseDateCountStatsSerializer):
    """
    Serializer for user statistics by date.

    Extends `BaseDateCountStatsSerializer` to provide a serializer specifically for user statistics that involve
    counting users based on a date, such as daily user registrations. This serializer is associated with the `User`
    model.
    """

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = User


class RoleCountUserStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for user statistics based on roles.

    This serializer is used to represent statistics related to users, specifically the count of users grouped by their
    roles. It utilizes a custom field for handling role representation to ensure that roles are displayed using their
    readable labels rather than their internal database values.
    """

    #: Field to represent the user's role with a readable label.
    label = CustomChoiceCharField(choices=UserRoleChoices, source='role')
    #: Field to represent the count of users with the respective role.
    count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('label', 'count')


class DateCountProfileStatsSerializer(BaseDateCountStatsSerializer):
    """
    Serializer for profile statistics by date.

    Extends `BaseDateCountStatsSerializer` to provide a serializer specifically for profile statistics that involve
    counting profiles based on a date, such as daily profile creations. This serializer is associated with the `Profile`
     model.

    Note:
        This serializer does not introduce new fields or methods but specifies the `Profile` model in the Meta class,
        making it specific to profile data.
    """

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = Profile


class InterestCountProfileStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for profile statistics based on interests.

    This serializer is designed to aggregate and represent statistics of profiles based on different interests. It
    leverages a custom choice field to display interest categories with human-readable labels, facilitating easier
    comprehension of the data in client applications.
    """

    #: Field to represent the profile's interest with a readable label.
    label = CustomChoiceCharField(choices=InterestChoices, source='interest')
    #:  Field to represent the count of profiles with the respective interest.
    count = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ('label', 'count')


class ReasonCountProfileStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for profile statistics based on reasons for joining.

    This serializer is tailored for summarizing profile data based on the reasons users have for joining or
    participating in the platform. It uses a custom field for the reason attribute to ensure that reasons are presented
    through their readable labels, enhancing the clarity of the output data.
    """

    #: Field to represent the profile's reason for joining with a readable label.
    label = CustomChoiceCharField(choices=ReasonChoices, source='reason')
    #: Field to represent the count of profiles with the respective reason.
    count = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ('label', 'count')
