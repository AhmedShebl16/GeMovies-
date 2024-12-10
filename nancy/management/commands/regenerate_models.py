# nancy/management/commands/regenerate_models.py
from django.core.management.base import BaseCommand
from nancy.models import Movie
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
import os

def normalize_string(s):
    """
    Normalize a string by removing hyphens and converting to lowercase.
    """
    return s.replace('-', '').lower()

class Command(BaseCommand):
    help = 'Regenerate similarity matrices for movie recommendations.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading movies from the database...")
        movies_qs = Movie.objects.all()
        movies_data = list(movies_qs.values())
        df_movies = pd.DataFrame(movies_data)

        # Normalize movie titles
        df_movies['normalized_title'] = df_movies['title'].apply(lambda x: normalize_string(x.lower()))

        self.stdout.write("Generating TF-IDF matrix...")
        tfidf = TfidfVectorizer(stop_words='english')
        df_movies['description'] = df_movies['description'].fillna('')
        tfidf_matrix = tfidf.fit_transform(df_movies['description'])

        self.stdout.write("Calculating cosine similarity...")
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        self.stdout.write("Creating indices mapping...")
        indices = pd.Series(df_movies.index, index=df_movies['normalized_title']).drop_duplicates()

        # Define model directory
        model_dir = os.path.join(settings.BASE_DIR, 'nancy', 'ml_models')
        os.makedirs(model_dir, exist_ok=True)

        # Save the models
        self.stdout.write("Saving cosine_sim.pkl...")
        with open(os.path.join(model_dir, 'cosine_sim.pkl'), 'wb') as f:
            pickle.dump(cosine_sim, f)

        self.stdout.write("Saving df_movies.pkl...")
        with open(os.path.join(model_dir, 'df_movies.pkl'), 'wb') as f:
            pickle.dump(df_movies, f)

        self.stdout.write("Saving indices.pkl...")
        with open(os.path.join(model_dir, 'indices.pkl'), 'wb') as f:
            pickle.dump(indices, f)

        self.stdout.write("Saving tfidf_vectorizer.pkl...")
        with open(os.path.join(model_dir, 'tfidf_vectorizer.pkl'), 'wb') as f:
            pickle.dump(tfidf, f)

        self.stdout.write(self.style.SUCCESS('Successfully regenerated similarity matrices.'))
