from django.contrib.auth.backends import get_user_model

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from ..models import Profile


User = get_user_model()


class ProfileSerializer(FlexFieldsModelSerializer):
    """
    Serializer for the Profile model, including dynamic fields and a custom age field.
    Utilizes FlexFieldsModelSerializer for expandable and dynamic field control.
    """
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        exclude = ()
        read_only_fields = ('id', 'user', 'create_at', 'update_at', 'age')
        expandable_fields = {
            'user': ('accounts.api.serializers.CustomUserSerializer', {'many': False, 'read_only': True,
                                                                       'omit': ['profile']}),
        }
