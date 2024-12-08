import random

from django.db import models
from django.contrib.auth.backends import get_user_model

import factory

from .enums import UserRoleChoices
from profiles.factories import ProfileFactory


User = get_user_model()


@factory.django.mute_signals(models.signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """
    UserFactory is a factory class for creating User model instances using factory_boy.

    This factory is configured to work with Django's ORM and uses various factory_boy features like LazyAttribute,
    Faker, LazyFunction, PostGenerationMethodCall, lazy_attribute_sequence, and post_generation hooks to create
    User model instances with appropriate attributes and related objects.
    """

    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    terms_and_condition = True
    role = factory.LazyFunction(lambda: random.choices(
        UserRoleChoices.choices,
        weights=[0, 100, 0, 0],
        k=1
    )[0][0])
    is_active = factory.LazyFunction(lambda: random.choices(
        [True, False],
        weights=[90, 10],
        k=1
    )[0])
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    class Meta:
        model = User

    @factory.lazy_attribute_sequence
    def username(self, n):
        """
        Generates a unique username for each User instance.

        Args:
            - n (int): A sequential number provided by factory_boy.

        Returns:
            - str: A unique username string.
        """
        max_pk = User.objects.aggregate(max_pk=models.Max('pk'))['max_pk'] or 0
        return f'user_{max(max_pk, n) + 1}'

    @factory.post_generation
    def post_create(self, create, extracted, **kwargs):
        """
        Post-generation hook to perform additional actions after a User instance is created.

        Specifically, if the created user has a role of CUSTOMER, a ProfileFactory is invoked to create an associated
        profile.

        Args:
            - create (bool): Indicates if the instance is being created (True) or built (False).
            - extracted (Any): Additional parameters passed to the factory.
            - **kwargs (dict): Arbitrary keyword arguments.
        """
        if create and self.role == UserRoleChoices.CUSTOMER and getattr(self, 'profile', None) is None:
            ProfileFactory(user=self)
