"""
Django Testing Utilities for Enhanced Productivity and Consistency

This file comprises a suite of mixin classes designed to augment and streamline the testing process within Django
applications. These mixins cater to a wide range of testing scenarios, from basic model validation to complex user
authentication flows. Each mixin is crafted to provide reusable, modular functionality that can be easily integrated
into test cases, thereby promoting code reusability and maintainability.

Key Features:
- `GenericTestCaseHelperMixin`: Offers generic utilities for asserting model field values and queryset evaluations,
  facilitating thorough model instance validations.
- `ModelTestCaseHelperMixin`: Extends testing capabilities to include model-specific operations, such as handling
  translation fields and dynamic field exclusion.
- `FactoryTestCaseHelperMixin`: Simplifies the creation and management of model instances for testing through factory
  patterns, supporting both single instance and batch generation.
- `UserFactoryTestCaseHelperMixin`: Tailors the factory mixin approach specifically for user model instances,
  incorporating default properties like user roles and activation status.
- `AuthTestCaseHelperMixin`: Provides a set of tools for generating and managing authentication tokens, essential for
  testing API endpoints requiring authenticated access.
- `UserTestCaseHelperMixin`: A comprehensive mixin that combines user instance generation with authentication handling,
  ideal for tests involving user operations and permissions.

Usage Guidelines:
- Mixins should be inherited by your test case classes to leverage their functionalities.
- Customization and extension of mixin functionalities are encouraged to fit specific testing needs.
- Ensure that your project's settings and dependencies are compatible with the utilities provided by these mixins.

Important Note:
- While these mixins aim to cover a broad range of testing scenarios, they may not address all possible cases. It's
important to assess their applicability to your specific project requirements and adjust or extend their functionalities
accordingly.
"""
from djoser import utils
from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.auth.tokens import default_token_generator

from modeltranslation.fields import TranslationField
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from ..enums import UserRoleChoices
from ..factories import UserFactory


class GenericTestCaseHelperMixin:
    """
    A mixin for generic test case helpers in Django.

    This mixin provides utility methods for Django model test cases, allowing for assertions on model instances,
    including field value checks, queryset comparisons, and more. It is designed to be used in test classes to
    streamline and standardize testing of Django models.
    """

    def assertModelFieldsNotNone(self, instance, exclude=None):
        """
        Asserts that all model fields of an instance are not None, excluding any fields specified.

        Args:
            - instance (models.Model): The Django model instance to check.
            - exclude (tuple, optional): A tuple of field names to exclude from the check.

        Raises:
            - AssertionError: If any of the included model fields are None.
        """
        # Refreshes the instance from the database, ensuring it has the most up-to-date values.
        instance.refresh_from_db()

        # Calls a method to retrieve a list of the model's field names, excluding any specified in the 'exclude' parameter.
        fields = self.get_model_fields(instance._meta.model, exclude)

        # Iterates over each field name in the list of model fields.
        for field in fields:
            # Retrieves the value of the current field from the instance.
            instance_value = getattr(instance, field, None)

            # Asserts that the value from the instance is not None.
            self.assertIsNotNone(instance_value, f'Filed {field} from {instance_value} is expected not to be None')

    def assertModelFields(self, instance, instance_dict, exclude=None):
        """
        Asserts that the values of an instance's fields match those in a provided dictionary.

        Args:
            - instance (models.Model): The Django model instance to check.
            - instance_dict (dict): A dictionary where keys are field names and values are the expected values.
            - exclude (tuple, optional): A tuple of field names to exclude from the check.

        Raises:
            - AssertionError: If any of the included model fields do not match the corresponding value in
              `instance_dict`.
       """
        # Refreshes the instance from the database, ensuring it has the most up-to-date values.
        instance.refresh_from_db()

        # Calls a method to retrieve a list of the model's field names, excluding any specified in the 'exclude' parameter.
        fields = self.get_model_fields(instance._meta.model, exclude)

        # Iterates over each field name in the list of model fields.
        for field in fields:
            # Retrieves the value of the current field from the instance.
            instance_value = getattr(instance, field, None)

            # Attempts to retrieve the value for the current field from the provided dictionary ('instance_dict').
            instance_dict_value = instance_dict.get(field)

            # Asserts that the value from the instance matches the value from the dictionary for the current field.
            # If they do not match, the assertion fails and raises an AssertionError, including a message
            # indicating which field mismatched and showing the expected vs. actual values.
            self.assertEqual(
                instance_value,
                instance_dict_value,
                f'Field \'{field}\' mismatch: expected {instance_value}, got {instance_dict_value}'
            )

    def assertQuerysetEqualList(self, queryset, queryset_list, exclude=None, sorting_field=None):
        """
        Asserts that a queryset is equivalent to a list of dictionaries, with optional field exclusion and sorting.

        Args:
            - queryset (QuerySet): The Django queryset to check.
            - queryset_list (list): A list of dictionaries representing the expected data.
            - exclude (tuple, optional): A tuple of field names to exclude from the check.
            - sorting_field (str, optional): The field name to sort both the queryset and the list by.

        Raises:
            - AssertionError: If the sorted queryset does not match the sorted list.
        """
        # Assert that the number of items in the queryset is equal to the number of items in the list.
        self.assertEqual(queryset.count(), len(queryset_list))

        # Set the default sorting field to 'id' if no sorting field is provided.
        if sorting_field is None:
            sorting_field = 'id'

        # Sort the list of dictionaries by the specified sorting field.
        sorted_list = sorted(queryset_list, key=lambda x: x[sorting_field])

        # Sort the queryset by the specified sorting field.
        sorted_queryset = queryset.order_by(sorting_field)

        # Iterate over pairs of instances from the sorted queryset and the sorted list.
        for inst, inst_dict in zip(sorted_queryset, sorted_list):
            # Call a method to assert that the fields of the model instance match the corresponding fields in the
            # dictionary, excluding any specified fields.
            self.assertModelFields(inst, inst_dict, exclude)

    def assertQuerysetContains(self, main_queryset, sub_queryset):
        """
        Asserts that all items in a sub-queryset are contained within a main queryset.

        Args:
            - main_queryset (QuerySet): The main queryset to check against.
            - sub_queryset (QuerySet): The queryset that should be fully contained within the main queryset.

        Raises:
            - AssertionError: If any items in `sub_queryset` are not found in `main_queryset`.
        """
        # Remove ordering from the querysets to prevent `ORDER BY` in subqueries
        main_queryset = main_queryset.order_by()
        sub_queryset = sub_queryset.order_by()

        # Use the `difference` method to find items in `sub_queryset` that are not in `main_queryset`
        diff_queryset = sub_queryset.difference(main_queryset)

        # Assert that `diff_queryset` does not exist, meaning `sub_queryset` is fully contained within `main_queryset`
        self.assertFalse(
            diff_queryset.exists(),
            f"Sub-queryset is not fully contained in the main queryset, differs {diff_queryset}."
        )

    @staticmethod
    def get_model_fields(model, exclude=None):
        """
        Retrieves a tuple of field names for a given model, excluding any specified fields.

        Args:
            - model (models.Model): The Django model to retrieve field names from.
            - exclude (tuple, optional): A tuple of field names to exclude.

        Returns:
            - tuple: A tuple of field names.
        """
        exclude = exclude or ()
        return tuple(
            filter(
                lambda field_name: field_name not in exclude,
                map(lambda field: field.name, model._meta.fields)
            )
        )

    @staticmethod
    def instance_to_dict(instance, fields=None, exclude=None):
        """
        Converts a model instance into a dictionary, with options to specify or exclude fields.

        Args:
            - instance (models.Model): The instance to convert.
            - fields (list, optional): A list of field names to include in the dictionary. If None, all fields are
              included.
            - exclude (tuple, optional): A tuple of field names to exclude from the dictionary.

        Returns:
            - dict: A dictionary representation of the instance.
        """
        return model_to_dict(
            instance,
            fields=fields,
            exclude=exclude
        )


class ModelTestCaseHelperMixin:
    """
    A mixin to assist with model-related test cases.

    This mixin provides a set of utilities for handling models in test cases, especially useful for  Django
    applications. It includes methods for retrieving the model under test, handling translation fields, onstructing
    querysets with optional filtering, and managing fields to exclude in various operations.
    """
    #: Placeholder for the model class associated with this mixin.
    model = None
    #: Fields to exclude by default in operations.
    exclude: tuple = ()
    #: Flag to indicate whether translation fields should be excluded.
    exclude_translations: bool = True

    def get_model(self):
        """
        Retrieves the model associated with this test case.

        Returns:
            - model (models.Model): The Django model class associated with this mixin. If not explicitly set, it will
              attempt to retrieve the model from a superclass.
        """
        if self.model:
            return self.model
        return super().get_model()

    def get_translation_fields(self):
        """
        Identifies and returns the translation fields of the model.

        Returns:
            - fields (tuple): A tuple containing the names of all translation fields in the model.
        """
        model = self.get_model()
        fields = filter(lambda field: isinstance(field, TranslationField), model._meta.fields)
        return tuple(map(lambda field: field.name, fields))

    def get_exclude(self):
        """
        Constructs a tuple of field names to be excluded, optionally including translation fields.

        Returns:
            - exclude (tuple): A tuple of field names to be excluded in operations, potentially augmented by translation
              fields based on the `exclude_translations` flag.
        """
        if not self.exclude_translations:
            return self.exclude
        return *self.exclude, *self.get_translation_fields()

    def get_queryset(self, **kwargs):
        """
        Constructs a queryset for the associated model, optionally filtered by provided keyword arguments.

        Args:
            - **kwargs (dict): Arbitrary keyword arguments used for filtering the queryset.

        Returns:
            - queryset (QuerySet): A Django queryset for the associated model, possibly filtered based on `kwargs`.
        """
        model = self.get_model()
        if kwargs:
            return model.objects.filter(**kwargs).distinct()
        return model.objects.all()


class FactoryTestCaseHelperMixin:
    """
    A mixin to assist with factory-based test cases.

    This mixin simplifies the creation of model instances for testing purposes using factories, particularly with
    Django's ORM. It provides methods to get the model class associated with a factory, to create single or multiple
    instances, and to optionally persist them to the database.
    """
    #: Placeholder for the factory class associated with this mixin.
    factory_class = None

    def get_model(self):
        """
        Retrieves the model class associated with the factory class.

        Returns:
            - model (models.Model): The Django model class associated with the factory_class. If factory_class
              is not set, attempts to retrieve the model from a superclass.
        """
        if self.factory_class:
            return self.factory_class._meta.model
        return super().get_model()

    def get_factory_class(self, factory_class=None):
        """
        Retrieves the factory class for creating model instances.

        Args:
            - factory_class (Factory, optional): An optional factory class. If not provided, the mixin's factory_class is used.

        Returns:
            - factory_class (Factory): The factory class used to create model instances.
        """
        if factory_class:
            return factory_class
        return self.factory_class

    def _generate_instance(self, factory_class=None, save=True, **kwargs):
        """
        Internal method to generate a single instance using the factory.

        Args:
            - factory_class (Factory, optional): The factory class to use. Defaults to the mixin's factory_class.
            - save (bool): Whether to save the instance to the database. Defaults to True.
            - **kwargs: Arbitrary keyword arguments passed to the factory for instance creation.

        Returns:
            - instance (models.Model): The generated model instance, either saved or unsaved based on the `save`
              argument.
        """
        factory_class = self.get_factory_class(factory_class)
        if save:
            return factory_class.create(**kwargs)
        return factory_class.build(**kwargs)

    def generate_instance(self, save=True, **kwargs):
        """
        Generates a single model instance using the factory, with an option to save it to the database.

        Args:
            - save (bool): Whether to save the instance to the database. Defaults to True.
            - **kwargs: Arbitrary keyword arguments passed to the factory for instance creation.

        Returns:
            - instance (models.Model): The generated model instance, either saved or unsaved based on the `save`
              argument.
        """
        return self._generate_instance(save=save, **kwargs)

    def _generate_instances(self, factory_class=None, size=10, save=True, **kwargs):
        """
        Internal method to generate multiple instances using the factory.

        Args:
            - factory_class (Factory, optional): The factory class to use. Defaults to the mixin's factory_class.
            - size (int): The number of instances to generate. Defaults to 10.
            - save (bool): Whether to save the instances to the database. Defaults to True.
            - **kwargs: Arbitrary keyword arguments passed to the factory for instance creation.

        Returns:
            - instances (list of models.Model): A list of generated model instances, either saved or unsaved based on
              the `save` argument.
        """
        factory_class = self.get_factory_class(factory_class)
        if save:
            return factory_class.create_batch(size=size, **kwargs)
        return factory_class.build_batch(size=size, **kwargs)

    def generate_instances(self, size=10, save=True, **kwargs):
        """
        Generates multiple model instances using the factory, with an option to save them to the database.

        Args:
            - size (int): The number of instances to generate. Defaults to 10.
            - save (bool): Whether to save the instances to the database. Defaults to True.
            - **kwargs: Arbitrary keyword arguments passed to the factory for instance creation.

        Returns:
            - instances (list of models.Model): A list of generated model instances, either saved or unsaved based on
              the `save` argument.
        """
        return self._generate_instances(size=size, save=save, **kwargs)


class UserFactoryTestCaseHelperMixin(FactoryTestCaseHelperMixin):
    """
    A mixin to assist with user model factory-based test cases.

    Extending the FactoryTestCaseHelperMixin, this mixin is specifically tailored for testing scenarios involving
    user models. It provides customized methods to generate user instances with default properties suitable for most
    tests, such as setting default roles and activation status.
    """
    #: The factory class for creating user model instances.
    user_factory_class = UserFactory

    def get_user_factory_class(self):
        """
        Retrieves the user factory class for creating user model instances.

        Returns:
            - user_factory_class (Factory): The factory class used to create user model instances.
        """
        return self.user_factory_class

    def generate_user(self, save=True, **kwargs):
        """
        Generates a single user instance with default properties, with an option to save it to the database.

        Args:
            - save (bool): Whether to save the instance to the database. Defaults to True.
            - **kwargs: Arbitrary keyword arguments passed to the user factory for instance creation. Defaults include
              setting the user role to `UserRoleChoices.CUSTOMER` and `is_active` to True.

        Returns:
            - user (models.Model): The generated user model instance, either saved or unsaved based on the `save`
              argument.
        """
        kwargs.setdefault('role', UserRoleChoices.CUSTOMER)
        kwargs.setdefault('is_active', True)
        return self._generate_instance(factory_class=self.get_user_factory_class(), save=save, **kwargs)

    def generate_users(self, size=10, save=True, **kwargs):
        """
        Generates multiple user instances with default properties, with an option to save them to the database.

        Args:
            - size (int): The number of user instances to generate. Defaults to 10.
            - save (bool): Whether to save the instances to the database. Defaults to True.
            - **kwargs: Arbitrary keyword arguments passed to the user factory for instance creation. `is_active` is
                        set to True by default.

        Returns:
            - users (list of models.Model): A list of generated user model instances, either saved or unsaved based on
              the `save` argument.
        """
        kwargs.setdefault('role', UserRoleChoices.CUSTOMER)
        kwargs.setdefault('is_active', True)
        return self._generate_instances(factory_class=self.get_user_factory_class(), size=size, save=save, **kwargs)


class AuthTestCaseHelperMixin:
    """
    A mixin providing authentication-related helper methods for test cases.

    This mixin includes methods for generating access and refresh tokens for a user, encoding user primary keys,
    generating default tokens, formatting authorization headers, and creating authorization headers with configurable
    token lifetimes. It's intended to simplify authentication processes in test cases, especially for APIs requiring
    token-based authentication.
    """

    @staticmethod
    def get_access_token(user):
        """
        Generates an access token for a given user.

        Args:
            - user (User): The user for whom to generate the access token.

        Returns:
            - access_token (str): The generated access token.
        """
        return AccessToken.for_user(user)

    @staticmethod
    def get_refresh_token(user):
        """
        Generates a refresh token for a given user.

        Args:
            - user (User): The user for whom to generate the refresh token.

        Returns:
            - refresh_token (str): The generated refresh token.
        """
        return RefreshToken.for_user(user)

    @staticmethod
    def encode_user_pk(pk):
        """
        Encodes a user's primary key (PK).

        Args:
            - pk (int or str): The primary key of the user to encode.

        Returns:
            - encoded_pk (str): The encoded primary key.
        """
        return utils.encode_uid(pk)

    @staticmethod
    def token_generator(user):
        """
        Generates a default token for a given user.

        Args:
            - user (User): The user for whom to generate the token.

        Returns:
            - token (str): The generated token.
        """
        return default_token_generator.make_token(user)

    @staticmethod
    def format_auth_header(token):
        """
        Formats an authentication token into an authorization header value.

        Args:
            - token (str): The token to format.

        Returns:
            - auth_header (str): The formatted authorization header value, including the header type (e.g., "JWT").
        """
        header = getattr(settings, 'AUTH_HEADER_TYPES', ['JWT'])[0]
        return f'{header} {token}'

    @classmethod
    def get_auth_header(cls, user, lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']):
        """
        Generates a complete authorization header for a given user, with an optional custom token lifetime.

        Args:
            - user (User): The user for whom to generate the authorization header.
            - lifetime (datetime.timedelta): The lifetime of the token. Defaults to the 'ACCESS_TOKEN_LIFETIME' setting
              from SIMPLE_JWT.

        Returns:
            - auth_header (str): The complete authorization header, ready to be used in HTTP requests.
        """
        access = cls.get_access_token(user)
        access.set_exp(lifetime=lifetime)
        return cls.format_auth_header(str(access))


class UserTestCaseHelperMixin(UserFactoryTestCaseHelperMixin, AuthTestCaseHelperMixin):
    """
    A comprehensive mixin for user-related test cases.

    This mixin combines the functionalities of UserFactoryTestCaseHelperMixin and AuthTestCaseHelperMixin to provide
    a wide array of user-related test utilities. It enables the generation of user instances (with customizable
    properties and quantities), handling of authentication tokens, and construction of auth headers for API testing.
    It is particularly useful for tests that require authenticated user contexts or specific user configurations.
    """
    #: The mixin inherits all methods from UserFactoryTestCaseHelperMixin and AuthTestCaseHelperMixin.
    #: If additional user-specific test case helper methods are needed, they can be defined here.
