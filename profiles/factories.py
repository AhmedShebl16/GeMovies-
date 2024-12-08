import random

from django.db import models

import factory

from accounts.enums import UserRoleChoices
from .models import Profile
from .enums import GenderChoices, InterestChoices, ReasonChoices


@factory.django.mute_signals(models.signals.post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """
    ProfileFactory is a factory class for creating Profile model instances using factory_boy.

    This factory is configured to work with Django's ORM and utilizes various factory_boy features such as SubFactory,
    LazyFunction, and Faker to create Profile model instances with realistic and varied data.
    """

    user = factory.SubFactory('accounts.factories.UserFactory', role=UserRoleChoices.CUSTOMER, profile=None)
    gender = factory.LazyFunction(lambda: random.choices(
        GenderChoices.choices,
        weights=[50, 50, 0],
        k=1
    )[0][0])
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=100)
    phone_number_1 = factory.Faker('phone_number')
    phone_number_2 = factory.Faker('phone_number')
    city = factory.Faker('city')
    country = factory.Faker('country')
    address = factory.Faker('address')
    interest = factory.LazyFunction(lambda: random.choice(InterestChoices.choices)[0])
    reason = factory.LazyFunction(lambda: random.choice(ReasonChoices.choices)[0])

    class Meta:
        model = Profile

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = kwargs.get('user', None)
        if user:
            try:
                profile = user.profile
                return profile
            except Profile.DoesNotExist:
                ...
        return super()._create(model_class, *args, **kwargs)
