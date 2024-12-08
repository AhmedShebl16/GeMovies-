Profiles App
============

Subpackages
-----------

.. toctree::
   :maxdepth: 3

   profiles.api
   profiles.tests


Custom Django Profiles App
--------------------------

The custom Django profiles app is designed to enrich user profiles with additional personal and contact information. It
encompasses functionalities crucial for storing and managing extended details beyond basic authentication, such as
gender, date of birth, contact numbers, and location.

App Tree Structure
^^^^^^^^^^^^^^^^^^

.. code-block:: text

    profiles/
    ├── api/
    │   ├── filters.py            # Implements filtering logic for profile queries.
    │   ├── serializers.py        # Handles serialization and deserialization of profile data.
    │   ├── urls.py               # Contains URL patterns for API endpoints.
    │   └── views.py              # Defines view logic for handling API requests.
    ├── tests/
    │   ├── __init__.py           # Implements testing utilities for profile-related test cases.
    │   ├── test_api_filters.py   # Implements testing for API filters.
    │   ├── test_api_views.py     # Implements testing for API views.
    │   ├── test_filters.py       # Implements testing for filters profiles based on age ranges.
    │   └── test_models.py        # Implements testing for models.
    ├── admin.py                  # Customizes profiles models in Django Admin.
    ├── apps.py                   # Configuration settings for the profiles app.
    ├── constants.py              # Defines a set of constants used for error messaging.
    ├── enums.py                  # Defines enumerations for consistent handling of choices and states.
    ├── factories.py              # Defines factory classes for consistent model instance creation.
    ├── filters.py                # Implements filtering logic in admin page for profile queries.
    └── models.py                 # Contains profile models, defining the structure of profile data.

This app acts as a vital extension to the user model in the Django project, enhancing user experience and providing a
more detailed user identity. Its focused structure and clear organization, such as the separation of personal details,
contact information, and interests, make it a targeted and efficient solution for comprehensive user profile
management.


profiles.admin
--------------

.. automodule:: profiles.admin
   :members:
   :undoc-members:
   :show-inheritance:


profiles.constants
------------------

.. automodule:: profiles.constants
   :members:
   :undoc-members:
   :show-inheritance:


profiles.enums
--------------

.. automodule:: profiles.enums
   :members:
   :undoc-members:
   :show-inheritance:


profiles.factories
------------------

.. automodule:: profiles.factories
   :members:
   :undoc-members:
   :show-inheritance:


profiles.filters
----------------

.. automodule:: profiles.filters
   :members:
   :undoc-members:
   :show-inheritance:


profiles.models
---------------

.. automodule:: profiles.models
   :members:
   :exclude-members: Profile
   :undoc-members:
   :show-inheritance:

   .. autoclass:: Profile
      :members:

      .. attribute:: user
         :type: models.OneToOneField

         OneToOneField linking this profile to a unique CustomerUser. Ensures a one-to-one relationship between the user and their profile. The profile is deleted if the associated CustomerUser is deleted (`on_delete=models.CASCADE`).

      .. attribute:: gender
         :type: models.PositiveSmallIntegerField

         PositiveSmallIntegerField representing the gender of the user. Utilizes choices from `GenderChoices`. This field is optional.

      .. attribute:: date_of_birth
         :type: models.DateField

         DateField to store the user's date of birth. This field is optional.

      .. attribute:: phone_number_1
         :type: PhoneNumberField

         PhoneNumberField to store the user's primary phone number. This field is optional.

      .. attribute:: phone_number_2
         :type: PhoneNumberField

         PhoneNumberField to store the user's secondary phone number. This field is also optional.

      .. attribute:: city
         :type: models.CharField

         CharField to store the city part of the user's current location. Allows up to 200 characters and is optional.

      .. attribute:: country
         :type: models.CharField

         CharField to store the country of the user's current location. Allows up to 200 characters and is optional.

      .. attribute:: address
         :type: models.CharField

         CharField to store the user's address. This field is optional and allows up to 200 characters.

      .. attribute:: interest
         :type: models.PositiveSmallIntegerField

         PositiveSmallIntegerField to store the user's interests. Utilizes choices from `InterestChoices` and defaults to 'OTHER'. This field is optional.

      .. attribute:: reason
         :type: models.PositiveSmallIntegerField

         PositiveSmallIntegerField to store the user's reasons for using the service or product. Utilizes choices from `ReasonChoices` and defaults to 'OTHER'. This field is optional.

      .. attribute:: create_at
         :type: models.DateTimeField

         DateTime field that automatically records the timestamp when the profile is created. This is important for administrative and tracking purposes.

      .. attribute:: update_at
         :type: models.DateTimeField

         DateTime field that automatically updates the timestamp each time the profile is modified. Ensures that any changes to the profile are tracked and recorded.
