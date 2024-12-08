Info App
========

Subpackages
-----------

.. toctree::
   :maxdepth: 3

   info.api
   info.management.commands
   info.tests


Custom Django Info App
----------------------

The custom Django info app is designed to provide general information, policies, team member details, and other
essential content to users. It encompasses functionalities crucial for disseminating and managing informational content
such as company policies, team bios, and general FAQs.

App Tree Structure
^^^^^^^^^^^^^^^^^^

.. code-block:: text

    info/
    ├── api/
    │   ├── filters.py                   # Implements filtering logic for info queries.
    │   ├── serializers.py               # Handles serialization and deserialization of info data.
    │   ├── urls.py                      # Contains URL patterns for API endpoints.
    │   └── views.py                     # Defines view logic for handling API requests.
    ├── management/
    │   ├── commands/
    │   │   ├── populate_dummy_data.py   # Populates the database with dummy data for testing or development purposes.
    │   └── └── prebuild.py              # Rewrites links and styles in html files as django format (usually with react)
    ├── tests/
    │   ├── __init__.py                  # Implements testing utilities for info-related test cases.
    │   ├── test_api_filters.py          # Implements testing for API filters.
    │   ├── test_api_views.py            # Implements testing for API views.
    │   └── test_models.py               # Implements testing for models.
    ├── admin.py                         # Customizes info models in Django Admin.
    ├── apps.py                          # Configuration settings for the info app.
    ├── factories.py                     # Defines factory classes for consistent model instance creation.
    ├── models.py                        # Contains info models, defining the structure of info data.
    ├── translation.py                   # Implements the translation logic of the app's model for multiple languages.
    └── utils.py                         # Utility module where reusable code pieces, such as helper functions.

This app serves as the central hub for information-related operations in the Django project, ensuring that users have
easy and efficient access to important information. Its modular structure and clear separation of concerns, such as
segregating API components from core content management functionalities, make it a robust and maintainable solution for
information dissemination.


info.admin
----------

.. automodule:: info.admin
   :members:
   :undoc-members:
   :show-inheritance:


info.factories
--------------

.. automodule:: info.factories
   :members:
   :undoc-members:
   :show-inheritance:


info.models
-----------

.. autoclass:: MainInfo
   :members: __str__, whatsapp_link

   .. attribute:: facebook
      :type: models.URLField

      URL field to store the Facebook link of the owner's company or website.

   .. attribute:: instagram
      :type: models.URLField

      URL field to store the Instagram link of the owner's company or website.

   .. attribute:: twitter
      :type: models.URLField

      URL field to store the Twitter link of the owner's company or website.

   .. attribute:: telegram
      :type: models.URLField

      URL field to store the Telegram link of the owner's company or website.

   .. attribute:: email
      :type: models.EmailField

      Email field to store the contact email of the owner's company or website.

   .. attribute:: whatsapp
      :type: PhoneNumberField

      Phone number field (optional) to store the WhatsApp number for contact.

   .. attribute:: why_us
      :type: models.TextField

      Text field (optional) for a descriptive text about why to choose the owner's company or website.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field to automatically store the timestamp when the record is created.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field to automatically update the timestamp each time the record is modified.

.. autoclass:: FAQs
   :members: __str__

   .. attribute:: quote
      :type: models.CharField

      CharField to store the question part of the FAQ. This field allows up to 1000 characters.

   .. attribute:: answer
      :type: models.TextField

      TextField to store the answer for the FAQ question.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field to automatically store the timestamp when the FAQ entry is created.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field to automatically update the timestamp each time the FAQ entry is modified.

.. autoclass:: AboutUs
   :members: __str__

   .. attribute:: title
      :type: models.CharField

      CharField to store the title of the "About Us" section. This field allows up to 500 characters, and is typically
      used as a headline or introduction to the section.

   .. attribute:: description
      :type: models.TextField

      TextField to store the detailed description for the "About Us" section. This field is used to provide
      comprehensive information about the organization or website.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field to automatically store the timestamp when the "About Us" entry is created. This helps in tracking
      the inception of the content.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field to automatically update the timestamp each time the "About Us" entry is modified. This is useful
      for keeping the content up-to-date.

.. autoclass:: TermsOfService
   :members: __str__

   .. attribute:: title
      :type: models.CharField

      CharField to store the title of the Terms of Service document. This field allows up to 500 characters and is
      typically used as the headline or title for the terms.

   .. attribute:: description
      :type: models.TextField

      TextField to store the detailed text of the Terms of Service. This field is used for the comprehensive
      description and articulation of the rules and guidelines for using the site's services.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field to automatically record the timestamp when the Terms of Service entry is initially created. This
      is important for tracking the introduction of the terms.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field to automatically update the timestamp each time the Terms of Service entry is modified. This
      ensures that changes and updates to the terms are properly recorded and timestamped.

.. autoclass:: CookiePolicy
   :members: __str__

   .. attribute:: title
      :type: models.CharField

      CharField to store the title of the Cookie Policy document. This field, allowing up to 500 characters, is
      typically used as the headline or title for the cookie policy.

   .. attribute:: description
      :type: models.TextField

      TextField to store the detailed text of the Cookie Policy. This field is essential for providing a comprehensive
      description of how cookies are used on the site, their purpose, and user implications.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field that automatically records the timestamp when the Cookie Policy entry is created. This helps in
      tracking the inception of the policy.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field that automatically updates the timestamp each time the Cookie Policy entry is modified. This
      ensures that any changes or updates to the policy are properly recorded with a timestamp.

.. autoclass:: ContactUs
   :members: __str__

   .. attribute:: first_name
      :type: models.CharField

      CharField to store the first name of the user submitting the contact form. This field allows up to 120 characters
      and is optional.

   .. attribute:: last_name
      :type: models.CharField

      CharField to store the last name of the user. Like the first name, this field allows up to 120 characters and is
      optional.

   .. attribute:: email
      :type: models.EmailField

      EmailField to store the user's email address. It is essential for communication or responses to the contact
      submission.

   .. attribute:: phone_number
      :type: PhoneNumberField

      PhoneNumberField to store the user's phone number. This field is used for contact purposes and may be used as an
      alternative to email communication.

   .. attribute:: subject
      :type: models.CharField

      CharField to store the subject of the contact submission. This field helps in categorizing the contact reason and
      allows up to 250 characters.

   .. attribute:: message
      :type: models.TextField

      TextField to store the actual message from the user. This is the main content of the contact submission.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field that automatically records the timestamp when the contact form is submitted. This is useful for
      tracking when the contact was initiated.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field that automatically updates the timestamp each time the contact information is modified. This helps
      in keeping a record of any changes made to the contact submission.

.. autoclass:: HeaderImage
   :members: __str__

   .. attribute:: alt
      :type: models.CharField

      CharField to store alternative text for the header image. This text is crucial for accessibility and SEO,
      conveying the purpose of the image as it relates to the content of a document or webpage. Allows up to 250
      characters.

   .. attribute:: image
      :type: models.ImageField

      ImageField to store the actual image file. This field is used for uploading images to be displayed as header
      images on the site. The images are stored in 'home/header' directory.

   .. attribute:: is_active
      :type: models.BooleanField

      BooleanField to indicate whether the image is active or not. When set to false, the image will not appear on the
      homepage, allowing for easy management of which images are displayed.

   .. attribute:: url
      :type: models.URLField

      URLField to store a hyperlink that the header image should link to (optional). This field is useful for
      redirecting users to related content or external sites when they click on the header image.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field that automatically records the timestamp when the header image is created. This is important for
      tracking when the image was added to the site.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field that automatically updates the timestamp each time the header image is modified. This is useful
      for keeping track of the most recent changes or updates to the image.

.. autoclass:: TeamMember
   :members: __str__

   .. attribute:: name
      :type: models.CharField

      CharField to store the team member's name. This field allows up to 100 characters and is essential for
      identifying the individual on the team.

   .. attribute:: position
      :type: models.CharField

      CharField to store the team member's position or role within the team or organization. This field also allows up
      to 100 characters and helps in defining the member's role.

   .. attribute:: about
      :type: models.TextField

      TextField to store a brief description or biography of the team member. This field is optional and can be used to
      provide more detailed information about the member's background, expertise, or role in the team.

   .. attribute:: image
      :type: models.ImageField

      ImageField to store the team member's image. Images are uploaded to the 'members/' directory, and this field is
      used to visually represent the team member on the site.

   .. attribute:: facebook
      :type: models.URLField

      URLField for storing the team member's Facebook profile link. This field is optional and can be left blank.

   .. attribute:: twitter
      :type: models.URLField

      URLField for storing the team member's Twitter profile link. This field is optional and can be left blank.

   .. attribute:: linkedin
      :type: models.URLField

      URLField for storing the team member's LinkedIn profile link. This field is optional and can be left blank.

   .. attribute:: github
      :type: models.URLField

      URLField for storing the team member's GitHub profile link. This field is optional and is particularly useful for
      tech teams.

   .. attribute:: join_date
      :type: models.DateField

      DateField to store the date when the team member joined the organization. This helps in tracking the tenure or
      duration of the member within the team.

   .. attribute:: is_active
      :type: models.BooleanField

      BooleanField to indicate whether the team member is currently active or not. This field is useful for managing
      the display of current versus former team members on the site.

   .. attribute:: create_at
      :type: models.DateTimeField

      DateTime field that automatically records the timestamp when the team member's record is created. This is
      important for administrative and tracking purposes.

   .. attribute:: update_at
      :type: models.DateTimeField

      DateTime field that automatically updates the timestamp each time the team member's record is modified. This
      ensures that any changes to the team member's profile are tracked and recorded.

.. autoclass:: News
   :members: __str__

   .. attribute:: title
      :type: models.CharField

      A field for the news article title. It is limited to 250 characters.

   .. attribute:: description
      :type: models.TextField

      A field for the news article content. It is a text field that allows for a more extensive article description.

   .. attribute:: date
      :type: models.DateField

      The publication date of the news article.

   .. attribute:: alt
      :type: models.CharField

      Alternative text for the news article image, meant to convey the "why" of the image as it relates to the content
      of a document or webpage. It is limited to 250 characters.

   .. attribute:: image
      :type: models.ImageField

      The associated image for the news article. The images are uploaded to the 'home/news' directory.

   .. attribute:: is_active
      :type: models.BooleanField

      A boolean flag to indicate whether the news article is currently active. It can be blank, null, or set to True by
      default.

   .. attribute:: create_at
      :type: models.DateTimeField

      The timestamp for when the news article was created. It is automatically set upon creation of the article.

   .. attribute:: update_at
      :type: models.DateTimeField

      The timestamp for when the news article was last updated. It is automatically updated whenever the article is saved.

.. autoclass:: Award
   :members: __str__

   .. attribute:: name
      :type: models.CharField

      The name of the award. This field is limited to 250 characters and is used to identify the award within the system.

   .. attribute:: organization
      :type: models.CharField

      The name of the organization that awarded the recognition. This field also has a maximum length of 250 characters.

   .. attribute:: description
      :type: models.TextField

      A detailed description of the award. This field is optional and can be left blank.

   .. attribute:: date
      :type: models.DateField

      The date on which the award was given. This field is used to record the specific date of the award.

   .. attribute:: image
      :type: models.ImageField

      An image associated with the award. Images are uploaded to the 'home/awards' directory. This field is used to
      visually represent the award on a website or application.

   .. attribute:: is_active
      :type: models.BooleanField

      A boolean field indicating whether the award is active or not. This can be used to control the visibility of the
      award on a website or application. It supports blank and null values and defaults to True.

   .. attribute:: create_at
      :type: models.DateTimeField

      The creation date of the award record. This field is automatically set to the current date and time when the
      award is first created.

   .. attribute:: update_at
      :type: models.DateTimeField

      The last update date of the award record. This field is automatically updated every time the award record is saved.

.. autoclass:: Partner
   :members:

   .. attribute:: name
      :type: models.CharField

      The name of the partner. This field is essential for identifying the partner within the system and is limited to
      250 characters.

   .. attribute:: description
      :type: models.TextField

      An optional field for providing a detailed description of the partner. This field can be left blank if no
      additional information is needed beyond the name and image.

   .. attribute:: image
      :type: models.ImageField

      The image associated with the partner. This field is used to visually represent the partner, typically on a
      website or in applications. The images are stored in the 'home/partners' directory.

   .. attribute:: is_active
      :type: models.BooleanField

      A boolean field that indicates whether the partner is currently active. This can be used to manage the visibility
      of partner records in applications. The field supports blank and null values and defaults to True, indicating
      active by default.

   .. attribute:: create_at
      :type: models.DateTimeField

      The creation timestamp of the partner record. This field is automatically set to the current date and time when a
      new partner record is created, helping to track when the partner was added to the system.

   .. attribute:: update_at
      :type: models.DateTimeField

      The timestamp of the last update to the partner record. This field is automatically updated every time the
      partner record is saved, allowing for tracking of the most recent changes.


info.translation
----------------

.. automodule:: info.translation
   :members:
   :undoc-members:
   :show-inheritance:

info.utils
----------

.. automodule:: info.utils
   :members:
   :undoc-members:
   :show-inheritance:
