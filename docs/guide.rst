**Getting Started**
===================


Installation
------------
1. Clone the repository::

    git clone https://github.com/Castus-Technologies-Inc/castus-platform.git

2. Install virtual environment package - outside project directory -, then activate it::

    pip install virtualenv
    virtualenv env
    env\Scripts\activate (Windows)
    source env/bin/activate (Linux/Mac)

3. Navigate to project directory, then install the requirements of the project by running::

    cd castus-platform
    pip install -r requirements.txt

4. Add .env file in core directory -discussed in configuration section-
5. Apply migrations on the database::

    python manage.py migrate

6. Run django server, then go to the local URL::

    python manage.py runserver

For the URL, use standard text as RST does not support direct link text like Markdown. You can mention the URL explicitly where needed.

Configuration
-------------

- **Basic configuration steps (settings.py)**

Please refer to the section in the core for more details: :ref:`core-settings`.

- **Environmental variables (.env)** ::

    # Settings / Core Configuration
    SECRET_KEY=YOUR_SECRET_KEY
    DEBUG=True
    ALLOWED_HOSTS=*,
    LANGUAGE_CODE=en-us
    TIME_ZONE=UTC

    # Database Configuration
    DATABASE_NAME=db_name
    DATABASE_USER=db_user
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

    # Email Configuration
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=YOUR_EMAIL_HOT
    EMAIL_PORT=465
    EMAIL_HOST_USER=YOUR_HOST_USER
    EMAIL_HOST_PASSWORD=YOUR_HOST_PASSWORD
    EMAIL_USE_TLS=False
    EMAIL_USE_SSL=True

    # Social Auth Configuration
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=YOUR_GOOGLE_OAUTH2_API_KEY
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=YOUR_GOOGLE_OAUTH2_API_SECRET
    SOCIAL_AUTH_FACEBOOK_KEY=YOUR_FACEBOOK_API_KEY
    SOCIAL_AUTH_FACEBOOK_SECRET=YOUR_FACEBOOK_API_SECRET

    # DJOSER Email Sending Configuration
    SEND_ACTIVATION_EMAIL=False
    SEND_CONFIRMATION_EMAIL=False
    USERNAME_CHANGED_EMAIL_CONFIRMATION=False
    PASSWORD_CHANGED_EMAIL_CONFIRMATION=False


Build The Docs
--------------

1. Create schema file for **API** docs::

    python manage.py spectacular --file docs/schema.yml

2. Go to the docs directory::

    cd docs

3. Create html files::

    make html

4. Open html file '_build\\index.html'
