Core
====

.. _core-settings:

core.settings file
------------------

The Django settings file is a central configuration hub for a Django project, defining crucial parameters like database
connections, installed apps, middleware, templates, and security considerations. Its role is pivotal in tailoring the
behavior and functionality of the application to specific requirements, making it foundational to the project's
operation and customization.

**Here are the most important configs:**

.. py:data:: REST_FRAMEWORK
   :module: core.settings

   Configures the Django Rest Framework (DRF) settings. This includes default permissions, authentication classes, pagination styles, and other DRF-specific settings.

.. py:data:: SIMPLE_JWT
   :module: core.settings

   Defines settings for the Simple JWT library, used for JSON Web Token authentication. This covers token lifetime,
   signing key, and algorithm specifications.

.. py:data:: DJOSER
   :module: core.settings

   Contains configuration for Djoser, providing Django Rest Framework views for actions like registration, login,
   logout, password reset, and account activation.

.. py:data:: SPECTACULAR_SETTINGS
   :module: core.settings

   Specifies settings for DRF-Spectacular, including schema generation settings for API documentation such as title,
   version, and description.

.. py:data:: JAZZMIN_SETTINGS
   :module: core.settings

   Configures the Jazzmin Django Admin theme settings, encompassing the theme, site title, login screen, and other UI
   elements for Django Admin.


core.urls file
--------------

This section documents the URL patterns used in the application. Each URL pattern is mapped to a specific Django app
for handling different aspects of the application.

- **Accounts API**

  .. code-block:: python

      path('api/accounts/', include('accounts.api.urls'), name='accounts')

  This URL pattern routes requests starting with ``api/accounts/`` to the URL configurations defined in the
  ``accounts.api.urls`` module. It's used for handling API requests related to user accounts, such as registration,
  login, and user management.

- **Profiles API**

  .. code-block:: python

      path('api/accounts/', include('profiles.api.urls'), name='profiles')

  This URL pattern, also starting with ``api/accounts/``, routes to the ``profiles.api.urls`` module. It handles API
  requests related to user profiles, including profile viewing and editing. Note the overlap in path with the Accounts API; this might be an error or intentional based on specific routing needs in the application.

- **Information API**

  .. code-block:: python

      path('api/info/', include('info.api.urls'), name='info')

  Requests starting with ``api/info/`` are routed to the ``info.api.urls`` module. This pattern is typically used for
  endpoints that provide general information, such as application details, version info, or other public data.

- **Stats API**

  .. code-block:: python

      path('api/stats/', include('stats.api.urls'), name='stats')

  This URL pattern routes requests starting with ``api/stats/`` to the URL configurations defined in the
  ``stats.api.urls`` module. It's used for handling API requests related to statistical data, such as retrieving,
  updating, and managing various statistics within the application.


- **Documentation APIs**

  .. code-block:: python

    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/yaml/', SpectacularJSONAPIView.as_view(), name='schema_yaml_view'),
    path('api/docs/schema/json/', SpectacularYAMLAPIView.as_view(), name='schema_json_view'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(), name='redoc_docs_view'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(), name='swagger_docs_view')

  These URL patterns in Django configure endpoints for API documentation, providing access to OpenAPI schema in various
  formats (YAML, JSON) and rendering them through interactive documentation interfaces like Redoc and Swagger UI.


**Django Rest Framework Spectacular**

| The views if offers collectively provide tools for auto-generating OpenAPI schema documentation for your Django project.
They offer various interfaces and formats including Swagger UI, Redoc UI, and JSON/YAML representations, enabling
efficient API exploration, documentation, and integration.

.. py:data:: SpectacularAPIView
   :module: drf_spectacular.views

   Generates the OpenAPI schema for a Django project in a machine-readable format, serving as a foundation for API
   documentation and exploration.

.. py:data:: SpectacularJSONAPIView
   :module: drf_spectacular.views

   Provides the OpenAPI schema in JSON format, useful for programmatic consumption and integration with other API tools.

.. py:data:: SpectacularYAMLAPIView
   :module: drf_spectacular.views

   Offers the OpenAPI schema in YAML format, preferred for its readability and ease of manual editing.

.. py:data:: SpectacularSwaggerView
   :module: drf_spectacular.views

   Renders the OpenAPI schema using Swagger UI, providing an interactive documentation interface for API endpoints.

.. py:data:: SpectacularRedocView
   :module: drf_spectacular.views

   Presents the OpenAPI schema through Redoc UI, offering an alternative aesthetic and organizational approach for API
   documentation.
