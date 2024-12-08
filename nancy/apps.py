# nancy/apps.py

from django.apps import AppConfig

class NancyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nancy'
    verbose_name = 'Nancy - Movie Recommendation Assistant'
