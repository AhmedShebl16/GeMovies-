# nancy/apps.py
from django.apps import AppConfig
import os
import pickle

class NancyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nancy'

    def ready(self):
        from . import recommendation
        model_dir = os.path.join(self.path, 'ml_models')
        try:
            with open(os.path.join(model_dir, 'cosine_sim.pkl'), 'rb') as f:
                recommendation.MODELS['cosine_sim'] = pickle.load(f)
            with open(os.path.join(model_dir, 'df_movies.pkl'), 'rb') as f:
                recommendation.MODELS['df_movies'] = pickle.load(f)
            with open(os.path.join(model_dir, 'indices.pkl'), 'rb') as f:
                recommendation.MODELS['indices'] = pickle.load(f)
            with open(os.path.join(model_dir, 'tfidf_vectorizer.pkl'), 'rb') as f:
                recommendation.MODELS['tfidf'] = pickle.load(f)
            print("Pre-trained models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")
