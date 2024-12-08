from django.contrib.auth.backends import get_user_model

from djoser.serializers import UserSerializer, UserCreateSerializer


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for creating users that extends Djoser's UserCreateSerializer.
    Adds additional 'role' field to the user creation process.
    """

    class Meta(UserCreateSerializer.Meta):
        # Extend the fields from UserCreateSerializer.Meta.fields by adding 'role'
        fields = (*UserCreateSerializer.Meta.fields, 'role')


class CustomUserSerializer(UserSerializer):
    """
    Serializer for user instances that extends Djoser's UserSerializer.
    Adds additional 'role' field to the user representation.
    """

    class Meta(UserSerializer.Meta):
        # Extend the fields from UserSerializer.Meta.fields by adding 'role'
        fields = (*UserSerializer.Meta.fields, 'role')
