import string
import random
from typing import List
from collections import OrderedDict

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

import requests
import factory
from faker import Faker

from .models import (MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, ContactUs, HeaderImage,
                     TeamMember, News, Award, Partner)


def get_languages() -> dict:
    """
    Generates a dictionary of language codes mapped to their respective locale codes.

    This function reads the available languages from the `MODELTRANSLATION_LANGUAGES` setting and maps each language
    code to a locale code. For English ('en'), the locale is set to 'en-US', for Arabic ('ar') it's 'ar-EG', and for
    other languages, the locale is constructed by combining the language code with its uppercase form.

    Returns:
        - dict: A dictionary where keys are language codes and values are corresponding locale codes.
    """
    return {
        lang: 'en-US' if lang == 'en' else 'ar-EG' if lang == 'ar' else f'{lang}-{lang.upper()}'
        for lang in getattr(settings, 'MODELTRANSLATION_LANGUAGES', [])
    }


def prepare_languages(languages: dict) -> OrderedDict:
    """
    Prepares language data for use with Faker by creating an ordered dictionary.

    This function takes a dictionary of languages, presumably returned by `get_languages`, and transforms it into an
    ordered dictionary where each value is an incremental integer starting from 1. This format is suitable for use
    with Faker, which requires an ordered set of locales with priority indicated by the integer value.

    Args:
        - languages (dict): A dictionary of language codes and their respective locale codes.

    Returns:
        - OrderedDict: An ordered dictionary where keys are language codes and values are integers starting from 1.
    """
    return OrderedDict({(code, i + 1) for i, (_, code) in enumerate(languages.items())})


LANGUAGES = get_languages()
FAKER_LANGUAGES = prepare_languages(LANGUAGES)
faker = Faker(FAKER_LANGUAGES)


def set_model_translations(instance: models.Model, fields_to_translate: List[str]) -> None:
    """
    Sets translations for specified fields of a Django model instance.

    For each language code defined in settings.LANGUAGES, this function generates fake text or sentences (depending
    on the field type) and sets them on the corresponding translated fields of the given model instance.

    Args:
        - instance (django.db.models.Model): The Django model instance to set translations on.
        - fields_to_translate (list of str): A list of field names to translate.
    """

    for lang_code, _ in settings.LANGUAGES:
        # Get the Faker instance for the current language
        curr_faker = faker[LANGUAGES.get(lang_code)]
        if curr_faker is None:
            continue  # Skip if no Faker instance is available for the language

        for field_name in fields_to_translate:
            # Construct the name of the translation field
            translation_field_name = f'{field_name}_{lang_code}'

            # Get the field from the model class
            field = getattr(instance.__class__, field_name, None)

            # Generate translation text based on the field type
            translation_text = curr_faker.text() if isinstance(field, models.TextField) else \
                curr_faker.sentence(nb_words=10)

            # Set the translation text on the instance
            setattr(instance, translation_field_name, translation_text)


class LoremPicsumImageField(factory.django.ImageField):
    """
    A custom factory field that generates an image by downloading it from Lorem Picsum.

    This field is designed for use in Django model factories to populate image fields with random images
    for testing or development purposes. The images are fetched from Lorem Picsum, a free service that provides
    random placeholder images. If the image fetching process fails, the field falls back to the default behavior
    of generating a simple dummy image.
    """

    #: Specifies the length of the filename for the generated image. Defaults to 10 characters.
    name_length: int = 10
    #: The base URL of the Lorem Picsum service. Used to construct the final URL for fetching images.
    base_url: str = 'https://picsum.photos/'

    def _generate_image_name(self, length: int) -> str:
        """
        Generates a random alphanumeric string to use as an image filename.

        Args:
            - length (int): The desired length of the filename.

        Returns:
            - str: A random alphanumeric string of the specified length.
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def fetch_image(self, width: int = 200, height: int = 200) -> bytes:
        """
        Fetches a random image from Lorem Picsum with the specified dimensions.

        Args:
            - width (int): The width of the desired image. Defaults to 200 pixels.
            - height (int): The height of the desired image. Defaults to 200 pixels.

        Returns:
            - bytes: The content of the fetched image.

        Raises:
            - Exception: If there is an error fetching the image from Lorem Picsum.
        """
        image_url = f'{self.base_url}{width}/{height}'
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch image: {e}")

    def _generate(self, create, attrs):
        """
        Overrides the default image generation method to fetch and return an image from Lorem Picsum.

        This method attempts to fetch an image from Lorem Picsum. If successful, it returns a ContentFile
        containing the image data. If any part of the process fails, it falls back to the superclass's _generate
        method, which generates a simple dummy image.

        Args:
            - create (bool): Indicates whether the instance is being created.
            - attrs (dict): Additional attributes that may be passed to the generator.

        Returns:
            - ContentFile: A ContentFile object containing the image data, with a randomly generated filename.
        """
        try:
            image_content = self.fetch_image()
            image_name = f"{self._generate_image_name(self.name_length)}.png"
            return ContentFile(image_content, name=image_name)
        except Exception as e:
            return super()._generate(create, attrs)


class MainInfoFactory(factory.django.DjangoModelFactory):
    """
    MainInfoFactory is a factory class for creating MainInfo model instances using factory_boy.

    This factory class is configured for Django's ORM and uses Faker to generate realistic data for various social media
    URLs, email, and phone number fields. It also includes a custom post-generation hook to set translations for
    specified fields.
    """

    facebook = factory.Faker('url')
    instagram = factory.Faker('url')
    twitter = factory.Faker('url')
    telegram = factory.Faker('url')
    email = factory.Faker('email')
    whatsapp = factory.Faker('phone_number')
    why_us = factory.Faker('text')

    class Meta:
        model = MainInfo

    @factory.post_generation
    def set_translations(self, create, extracted, **kwargs):
        """
        A post-generation method to set translations for specific fields of the MainInfo instance.

        This method is called after a MainInfo instance is created. It uses the `set_model_translations` function
        to automatically set translations for the 'why_us' field based on the languages defined in settings.

        Args:
            - create (bool): Indicates if the instance is being created (True) or built (False).
            - extracted (Any): Additional parameters passed to the factory.
            - **kwargs (dict): Arbitrary keyword arguments.
        """

        if create:
            set_model_translations(self, ['why_us'])
            self.save()


class FAQsFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating FAQ instances for testing or development purposes.

    This factory uses the Faker library to generate random sentences for the `quote` field and random text for the
    `answer` field. It is intended for use with the FAQs model, allowing for the automated generation of FAQ data that
    can be used in testing environments or for initial data loading during development.
    """

    quote = factory.Faker('sentence', nb_words=10)
    answer = factory.Faker('text')

    class Meta:
        model = FAQs


class TitledDescriptiveFactory(factory.django.DjangoModelFactory):
    """
    TitledDescriptiveFactory is a factory class for creating Django model instances that include 'title' and
    'description' fields, using factory_boy.

    This factory class is tailored for Django models that contain title and description fields requiring
    translations. It includes a custom post-generation hook to set translations for these fields.

    Note:
        The specific model to be associated with this factory should be set in a subclass, as this class does not
        directly specify a model in its Meta class. This makes the factory reusable for any model with title and
        description fields.

    Usage:
        To use this factory, subclass it and specify the model and any additional fields in the subclass.
    """

    @factory.post_generation
    def set_translations(self, create, extracted, **kwargs):
        """
        A post-generation method to set translations for the 'title' and 'description' fields of the model instance.

        This method is invoked after a model instance is created. It uses the `set_model_translations` function
        to automatically generate and set translations for the 'title' and 'description' fields based on the
        languages defined in settings.

        Args:
            - create (bool): Indicates if the instance is being created (True) or built (False).
            - extracted (Any): Additional parameters passed to the factory.
            - **kwargs (dict): Arbitrary keyword arguments.
        """

        if create:
            # Set translations for the 'title' and 'description' fields
            set_model_translations(self, ['title', 'description'])
            # Save the instance with translations
            self.save()


class AboutUsFactory(TitledDescriptiveFactory):
    """
    AboutUsFactory is a subclass of TitledDescriptiveFactory specifically for creating instances of the AboutUs model.

    This factory inherits the functionality of TitledDescriptiveFactory, particularly the post-generation method
    to set translations for 'title' and 'description' fields. It is specifically tailored to work with the AboutUs
    model in a Django application.
    """

    class Meta:
        model = AboutUs


class TermsOfServiceFactory(TitledDescriptiveFactory):
    """
    TermsOfServiceFactory is a subclass of TitledDescriptiveFactory specifically for creating instances of the
    TermsOfService model.

    This factory inherits the functionality of TitledDescriptiveFactory, including the automatic setting of
    translations for 'title' and 'description' fields. It is intended for use with the TermsOfService model
    in a Django application.
    """

    class Meta:
        model = TermsOfService


class CookiePolicyFactory(TitledDescriptiveFactory):
    """
    CookiePolicyFactory is a subclass of TitledDescriptiveFactory specifically for creating instances of the
    CookiePolicy model.

    Inheriting from TitledDescriptiveFactory, this factory class is equipped to handle the creation of CookiePolicy
    model instances, including setting translations for 'title' and 'description' fields. It is designed for use
    within a Django application.
    """

    class Meta:
        model = CookiePolicy


class PrivacyPolicyFactory(TitledDescriptiveFactory):
    """
    PrivacyPolicyFactory is a subclass of TitledDescriptiveFactory specifically for creating instances of the
    PrivacyPolicy model.

    As with other subclasses of TitledDescriptiveFactory, this factory is focused on generating PrivacyPolicy model
    instances, complete with automatically translated 'title' and 'description' fields. It is intended for Django
    applications.
    """

    class Meta:
        model = PrivacyPolicy


class ContactUsFactory(factory.django.DjangoModelFactory):
    """
    ContactUsFactory is a factory class for creating instances of the ContactUs model using factory_boy.

    This factory class is designed for the Django ORM and uses Faker to generate realistic data for fields like
    first name, last name, email, phone number, subject, and message. It's ideal for testing and seeding development
    databases with data that resembles real user inquiries.

    Meta:
        model (ContactUs): Specifies the ContactUs model to which this factory is associated.
    """

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    subject = factory.Faker('sentence', nb_words=4)
    message = factory.Faker('text')

    class Meta:
        model = ContactUs


class HeaderImageFactory(factory.django.DjangoModelFactory):
    """
    HeaderImageFactory is a factory class for creating instances of the HeaderImage model using factory_boy.

    This class leverages Django's ORM in conjunction with Faker and factory_boy's image generation capabilities to
    create HeaderImage model instances. These instances include fields like alternative text for the image, the image
    itself, an active status flag, and a URL.

    Meta:
        model (HeaderImage): Specifies the HeaderImage model to which this factory is associated.
    """

    title = factory.Faker('sentence', nb_words=10)
    description = factory.Faker('text')
    alt = factory.Faker('sentence', nb_words=6)
    image = LoremPicsumImageField(color='blue')
    is_active = factory.Faker('boolean')
    url = factory.Faker('url')

    class Meta:
        model = HeaderImage


class TeamMemberFactory(factory.django.DjangoModelFactory):
    """
    TeamMemberFactory is a factory class for creating instances of the TeamMember model using factory_boy.

    This factory is intended for Django applications and utilizes Faker for generating realistic and diverse data
    for team member profiles. It's particularly useful for testing, seeding databases, or generating sample data
    for development purposes.

    Meta:
        model (TeamMember): Specifies the TeamMember model to which this factory is associated.
    """

    name = factory.Faker('name')
    position = factory.Faker('job')
    about = factory.Faker('text')
    image = LoremPicsumImageField(color='blue')
    facebook = factory.Faker('url')
    twitter = factory.Faker('url')
    linkedin = factory.Faker('url')
    github = factory.Faker('url')
    join_date = factory.Faker('past_date', start_date="-1y")
    is_active = factory.Faker('boolean')

    class Meta:
        model = TeamMember


class NewsFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating News instances for testing or development.

    Utilizes the Faker library to generate random but plausible data for news articles, including titles, descriptions,
    publication dates, and alternative text for images. Images are generated using the LoremPicsumImageField, which
    fetches random images from Lorem Picsum. Active status is randomly set to either true or false.
    """

    title = factory.Faker('sentence', nb_words=10)
    description = factory.Faker('text')
    date = factory.Faker('date')
    alt = factory.Faker('sentence', nb_words=6)
    image = LoremPicsumImageField(color='blue')
    is_active = factory.Faker('boolean')

    class Meta:
        model = News


class AwardFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating Award instances for use in testing or development environments.

    This factory uses Faker to generate realistic names, organizations, descriptions, and dates, and the
    LoremPicsumImageField to fetch placeholder images for awards. The active status of each award is randomly determined.
    """

    name = factory.Faker('word')
    organization = factory.Faker('company')
    description = factory.Faker('text')
    date = factory.Faker('date')
    image = LoremPicsumImageField(color='blue')
    is_active = factory.Faker('boolean')

    class Meta:
        model = Award


class PartnerFactory(factory.django.DjangoModelFactory):
    """
    A factory for generating Partner instances, suitable for testing and development.

    Uses Faker to create partner names and descriptions, and LoremPicsumImageField to obtain placeholder images.
    The is_active field is randomly set to true or false to reflect the active status of a partner.
    """

    name = factory.Faker('word')
    description = factory.Faker('text')
    image = LoremPicsumImageField(color='blue')
    is_active = factory.Faker('boolean')

    class Meta:
        model = Partner
