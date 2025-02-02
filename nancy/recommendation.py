# nancy/recommendation.py
import pickle
from django.conf import settings
import os
from .models import Movie
import pandas as pd
from .nlp_utils import normalize_string
import random

# Initialize a dictionary to hold models
MODELS = {}

def load_models():
    """
    Load pre-trained models from the ml_models directory.
    """
    model_dir = os.path.join(settings.BASE_DIR, 'nancy', 'ml_models')
    try:
        with open(os.path.join(model_dir, 'cosine_sim.pkl'), 'rb') as f:
            MODELS['cosine_sim'] = pickle.load(f)
        with open(os.path.join(model_dir, 'df_movies.pkl'), 'rb') as f:
            MODELS['df_movies'] = pickle.load(f)
        with open(os.path.join(model_dir, 'indices.pkl'), 'rb') as f:
            MODELS['indices'] = pickle.load(f)
        with open(os.path.join(model_dir, 'tfidf_vectorizer.pkl'), 'rb') as f:
            MODELS['tfidf'] = pickle.load(f)
        print("Pre-trained models loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")

# Load models when the module is imported
load_models()

def generate_recommendations(parsed_query):
    """
    Generates a list of recommended movies based on the parsed query.
    Introduces randomness to provide varied recommendations.
    """
    recommendations = set()

    # Recommend based on specific movies
    specific_movies = parsed_query.get('specific_movies', [])
    if specific_movies and all(k in MODELS for k in ('cosine_sim', 'df_movies', 'indices')):
        cosine_sim = MODELS['cosine_sim']
        df_movies = MODELS['df_movies']
        indices = MODELS['indices']
        for movie in specific_movies:
            movie_normalized = normalize_string(movie)
            if movie_normalized in indices:
                idx = indices[movie_normalized]
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:11]  # Exclude the movie itself
                for i, score in sim_scores:
                    recommendations.add(df_movies.iloc[i]['title'])

    # Recommend based on genres with randomness
    genres = parsed_query.get('genres', [])
    if genres and 'df_movies' in MODELS:
        df_movies = MODELS['df_movies']
        for genre in genres:
            genre_recs = df_movies[df_movies['genres'].str.contains(genre, case=False, na=False)]['title'].tolist()
            if genre_recs:
                # Shuffle the list to introduce randomness
                random.shuffle(genre_recs)
                # Select a subset (e.g., first 10 after shuffling)
                selected_genre_recs = genre_recs[:10]
                recommendations.update(selected_genre_recs)

    # Recommend based on actors with randomness
    actors = parsed_query.get('actors', [])
    if actors and 'df_movies' in MODELS:
        df_movies = MODELS['df_movies']
        for actor in actors:
            actor_recs = df_movies[df_movies['actors'].str.contains(actor, case=False, na=False)]['title'].tolist()
            if actor_recs:
                # Shuffle the list to introduce randomness
                random.shuffle(actor_recs)
                # Select a subset (e.g., first 10 after shuffling)
                selected_actor_recs = actor_recs[:10]
                recommendations.update(selected_actor_recs)

    # Recommend based on directors with randomness
    directors = parsed_query.get('directors', [])
    if directors and 'df_movies' in MODELS:
        df_movies = MODELS['df_movies']
        for director in directors:
            director_recs = df_movies[df_movies['directors'].str.contains(director, case=False, na=False)]['title'].tolist()
            if director_recs:
                # Shuffle the list to introduce randomness
                random.shuffle(director_recs)
                # Select a subset (e.g., first 10 after shuffling)
                selected_director_recs = director_recs[:10]
                recommendations.update(selected_director_recs)


    for movie in specific_movies:
        recommendations.discard(movie)

    return list(recommendations)
