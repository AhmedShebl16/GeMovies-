# nancy/management/commands/load_movies.py
import pickle
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Load pre-trained ML models into the application.'

    def handle(self, *args, **kwargs):
        model_files = ['cosine_sim.pkl', 'df_movies.pkl', 'indices.pkl', 'tfidf_vectorizer.pkl']
        missing_files = []
        for file in model_files:
            file_path = os.path.join(settings.BASE_DIR, 'nancy', 'ml_models', file)
            if not os.path.exists(file_path):
                missing_files.append(file)

        if missing_files:
            self.stdout.write(self.style.ERROR(f"Missing model files: {', '.join(missing_files)}"))
        else:
            self.stdout.write(self.style.SUCCESS("All pre-trained model files are present."))
