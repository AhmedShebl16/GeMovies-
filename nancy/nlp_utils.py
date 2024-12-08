# nancy/nlp_utils.py

import re


def parse_query(query):
    """
    Simple NLP parsing to extract genres, specific movie names, actors, and directors.
    This is a basic implementation. For more accurate parsing, consider using NLP libraries like SpaCy or NLTK.
    """
    # Define possible genres, actors, and directors (extend as needed)
    genres_list = [
        'action', 'comedy', 'drama', 'thriller', 'horror',
        'sci-fi', 'romantic', 'adventure', 'fantasy', 'documentary'
    ]

    # Patterns to extract entities
    genre_pattern = re.compile(r'\b(' + '|'.join(genres_list) + r')\b', re.IGNORECASE)
    movie_pattern = re.compile(r'similar to ([A-Za-z\s]+)', re.IGNORECASE)
    actor_pattern = re.compile(r'starring ([A-Za-z\s]+)', re.IGNORECASE)
    director_pattern = re.compile(r'directed by ([A-Za-z\s]+)', re.IGNORECASE)

    genres = genre_pattern.findall(query)
    specific_movies = movie_pattern.findall(query)
    actors = actor_pattern.findall(query)
    directors = director_pattern.findall(query)

    # Clean extracted data
    genres = [genre.lower() for genre in genres]
    specific_movies = [movie.strip() for movie in specific_movies]
    actors = [actor.strip() for actor in actors]
    directors = [director.strip() for director in directors]

    return {
        'genres': genres,
        'specific_movies': specific_movies,
        'actors': actors,
        'directors': directors
    }
