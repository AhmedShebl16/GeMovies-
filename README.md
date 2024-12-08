![Design](C:\Users\amfsh\Desktop\My Nancy\GeMovies-backend\static\images\logo-circle.png)
# GeMovies Platform
Embark on a cinematic journey with GeMovies, where our AI-driven platform tailors a world of movies perfectly suited to your tastes. Discover, explore, and immerse yourself in a personalized film adventure like no other.
## Installation

1. Clone the repository:
   ```shell
   git clone https://github.com/Castus-Technologies-Inc/castus-platform.git
   ```
2. Install virtual environment package - outside project directory -, then activate it:
    ```shell
    pip install virtualenv
    virtualenv env 
    env\Scripts\activate (Windows)
    source env/bin/activate (Linux/Mac) 
    ```
3. Navigate to project directory, then install the requirements of the project by running:
    ```shell
    cd GeMovies-backend
    pip install -r requirements.txt
    ```
4. Add .env file as following:
   ```.env
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
   ```
5. Apply migrations on the database:
    ```shell
    python manage.py migrate
    ```
5. Run django server, then got the local [url](http://127.0.0.1:8000/):
    ```shell
    python manage.py runserver 
    ```
 