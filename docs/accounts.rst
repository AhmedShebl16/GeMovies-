Accounts App
============


Subpackages
-----------

.. toctree::
   :maxdepth: 3

   accounts.api
   accounts.tests


Custom Django Accounts App
--------------------------

The custom Django ``accounts`` app is designed for comprehensive user authentication and management. It encompasses
functionalities essential for user account operations such as creation, updating, deletion, and password recovery.

App Tree Structure
^^^^^^^^^^^^^^^^^^

.. code-block:: text

    accounts/
    ├── api/
    │   ├── filters.py            # Implements filtering logic for user queries.
    │   ├── mixins.py             # Provides reusable class-based components for views.
    │   ├── permissions.py        # Defines custom permissions for API access control.
    │   ├── serializers.py        # Handles serialization and deserialization of user data.
    │   ├── urls.py               # Contains URL patterns for API endpoints.
    │   └── views.py              # Defines view logic for handling API requests.
    ├── tests/
    │   ├── __init__.py           # Implements testing utilities for enhanced productivity and consistency.
    │   ├── test_admin.py         # Implements testing for user model admin.
    │   ├── test_api_filters.py   # Implements testing for API filters.
    │   ├── test_api_views.py     # Implements testing for API views.
    │   ├── test_models.py        # Implements testing for models.
    │   └── test_signals.py       # Implements testing for user deactivation signal.
    ├── admin.py                  # Customizes user models in Django Admin.
    ├── apps.py                   # Configuration settings for the accounts app.
    ├── constants.py              # Defines a set of constants used for error messaging.
    ├── email.py                  # Manages email functionalities, including password reset emails.
    ├── enums.py                  # Defines enumerations for consistent handling of choices and states.
    ├── factories.py              # Defines factory classes for consistent model instance creation.
    ├── mixins.py                 # Provides mixins for common behaviors across the app.
    ├── models.py                 # Contains user models, defining the structure of user data.
    ├── signals.py                # Implements Django signals for user-related events.
    ├── urls.py                   # Configures URL patterns for the app's views.
    └── validators.py             # Provides custom validation logic for user data.

This app serves as the backbone for user-related operations in the Django project, ensuring secure and efficient user
account management. Its modular structure and clear separation of concerns, such as separating API components from core
functionalities, make it robust and maintainable.


accounts.admin
--------------
**Custom User Admin** class to give it more capabilities, such as actions, filters, search ...etc

.. automodule:: accounts.admin
    :members:
    :show-inheritance:


accounts.constants
------------------

.. automodule:: accounts.constants
    :members:
    :show-inheritance:


accounts.email
--------------
This Python file is pivotal in a Django-based web application, focusing on managing and customizing email communications:

1. **AttachMainInfoEmailMixin**: A mixin class that enriches email template contexts with 'main info' from the
   `MainInfo` model. This addition allows every email sent to include crucial, consistent information, enhancing
   personalization and relevance.

2. **Custom Email Classes**: The file defines various custom email classes (like `CustomActivationEmail`,
   `CustomConfirmationEmail`, etc.), each extending `AttachMainInfoEmailMixin` and Djoser email classes. They represent
   different types of email communications (account activation, password reset, etc.) and include 'main info' in their
   context, ensuring functionally relevant and application-specific content in automated emails.

3. **Integration with Djoser**: Utilizing Djoser email classes for base customization indicates reliance on Djoser for
   user management. Djoser, a popular Django library, handles user authentication tasks. Customizing its emails allows
   the application to maintain Djoser's robustness and security while tailoring the user experience to the
   application's specific needs.

4. **Template Specification**: The file specifies template paths for various emails (e.g., `template_name =
   "email/delete.html"` in `DeleteEmail`), indicating a separation of concerns. Email content and structure are managed
   through templates, facilitating easier updates and maintenance of email layouts and styles.

Overall, this file significantly enhances user experience through personalized, consistent email communication.
Automated emails are made informative, functional, and tailored, reflecting the application's unique context and
improving user engagement and professionalism.

.. automodule:: accounts.email
   :members:
   :undoc-members:


How it works?
^^^^^^^^^^^^^
.. image:: /static/images/email_flow.png

**Activation Email (CustomActivationEmail)**

1. *User Registers*: A new user completes the registration form on your application.
2. *Account Created*: The application creates the account but sets it as inactive.
3. *Sending Activation Email*: The `CustomActivationEmail` class is used to send an activation email with a unique link
   or token.
4. *User Activates Account*: The user clicks the link in the email, activating their account.

**Confirmation Email (CustomConfirmationEmail)**

1. *User Activates Account*: After clicking the activation link sent previously.
2. *Confirmation Triggered*: The application marks the account as active.
3. *Sending Confirmation Email*: The `CustomConfirmationEmail` class sends an email confirming the successful
   activation of the account.

**Password Reset Email (CustomPasswordResetEmail)**

1. *User Requests Password Reset*: The user clicks on "Forgot Password?" and submits their email.
2. *Sending Reset Email*: The application, using `CustomPasswordResetEmail`, sends an email with a password reset link.
3. *User Resets Password*: The user follows the link to create a new password.

**Password Changed Confirmation Email (CustomPasswordChangedConfirmationEmail)**

1. *User Changes Password*: After successfully resetting their password.
2. *Confirmation Email Sent*: The application sends a confirmation email using `CustomPasswordChangedConfirmationEmail`,
   confirming the change.

**Username Changed Confirmation Email (CustomUsernameChangedConfirmationEmail)**

1. *User Changes Username*: The user updates their username in the application settings.
2. *Sending Confirmation Email*: The `CustomUsernameChangedConfirmationEmail` sends a confirmation email, acknowledging
   the username change.

**Username Reset Email (CustomUsernameResetEmail)**

1. *Username Reset Request*: Similar to a password reset, the user requests a username reminder/reset.
2. *Sending Reset Email*: The application uses `CustomUsernameResetEmail` to send instructions or a reminder of the username.

**Delete Email (DeleteEmail)**

1. *User Deletes Account*: The user chooses to delete their account through the application settings.
2. *Sending Delete Confirmation Email*: Upon successful deletion, the application sends a confirmation email using
   `DeleteEmail`, confirming the account deletion.


accounts.enums
--------------

.. automodule:: accounts.enums
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: classproperty


accounts.factories
-------------------

.. automodule:: accounts.factories
   :members:
   :undoc-members:
   :show-inheritance:


accounts.mixins
---------------

.. automodule:: accounts.mixins
   :members:
   :undoc-members:
   :show-inheritance:


accounts.models
---------------

.. automodule:: accounts.models
   :members:
   :exclude-members: User
   :undoc-members:
   :show-inheritance:

   .. autoclass:: User
      :members: __str__, get_full_name, get_short_name

      .. attribute:: username
         :type: models.CharField

         Unique identifier for the user. Used for authentication and login. This field is required and has a maximum
         length of 150 characters.

      .. attribute:: first_name
         :type: models.CharField

         The user's first name. This field is optional and can be left blank. It has a maximum length of 30 characters.

      .. attribute:: last_name
         :type: models.CharField

         The user's last name. Similar to `first_name`, this field is optional and can be left blank. It has a maximum
         length of 150 characters.

      .. attribute:: role
         :type: models.PositiveSmallIntegerField

         Defines the role of the user within the application, such as 'admin', 'customer', or 'company'.

      .. attribute:: email
         :type: models.EmailField

         User's email address. It is used for communication and, depending on the configuration, possibly for login as
         well. This field must be unique.

      .. attribute:: password
         :type: models.CharField

         Hashed password for the user account, used for authentication. The field has a maximum length of 128
         characters.

      .. attribute:: is_superuser
         :type: models.BooleanField

         A boolean flag indicating whether the user has superuser status. A superuser has full access to the site and
         all models. Typically, this user can create, modify, and delete any data across all apps in the Django admin
         interface. This field is essential for administrative access and control. Defaults to `False`.

      .. attribute:: is_staff
         :type: models.BooleanField

         Flag indicating whether the user can access the Django admin site. Defaults to `False`.

      .. attribute:: is_active
         :type: models.BooleanField

         Flag indicating whether the user's account is currently active. Inactive accounts cannot log in. Defaults to
         `True`.

      .. attribute:: date_joined
         :type: models.DateTimeField

         The date and time when the account was created. This field is automatically set when the account is created.

      .. attribute:: last_login
         :type: models.DateTimeField

         The date and time of the user's last successful login. This field is automatically managed by Django and is
         updated whenever the user logs in. It is useful for tracking user activity and engagement.

      .. attribute:: terms_and_conditions
         :type: models.BooleanField

         Indicates whether the user has agreed to the terms and conditions of the service. Defaults to `False`.


accounts.signals
----------------

.. automodule:: accounts.signals
   :members:
   :undoc-members:
   :show-inheritance:

How it works?
^^^^^^^^^^^^^

1. **User Requests Email Change**: A user initiates an email address change request.
2. **Account Deactivation**: The user's account is temporarily deactivated for security during the email change process.
3. **Sending the Signal**: The `user_deactivated` signal is sent post-deactivation, triggering responses in other parts
   of the application, such as logging events or halting operations.
4. **Reactivation Through New Email**: The user receives an activation link at their new email, and upon confirmation,
   the account is reactivated.


accounts.utils
--------------

.. automodule:: accounts.utils
   :members:
   :undoc-members:
   :show-inheritance:


accounts.validators
-------------------

.. automodule:: accounts.validators
   :members:
   :undoc-members:
   :show-inheritance:
