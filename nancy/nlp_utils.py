# nancy/nlp_utils.py
import spacy
from fuzzywuzzy import process
from nltk.corpus import stopwords
import re
from .models import Movie
import logging

logger = logging.getLogger(__name__)

# Initialize SpaCy model
nlp = spacy.load('en_core_web_sm')

# Define genres list
GENRES_LIST = [
    'action', 'comedy', 'drama', 'thriller', 'horror',
    'sci-fi', 'romantic', 'adventure', 'fantasy', 'documentary',
    'animation', 'mystery', 'crime', 'biography', 'family', 'musical',
    'war', 'western', 'history', 'sport'
]

# Genre variations mapping
GENRE_VARIATIONS = {
    'thrilling': 'thriller',
    'action-packed': 'action',
    'romantic': 'romantic',
    'comedic': 'comedy',
    'horrifying': 'horror',
    'sci fi': 'sci-fi',
    'science fiction': 'sci-fi',
    'romantic comedy': 'romantic',
    'adventurous': 'adventure',
    'fantastical': 'fantasy',
    # Add more variations as needed
}

# Stopwords
STOP_WORDS = set(stopwords.words('english'))


def normalize_string(s):
    """
    Normalize a string by removing hyphens and converting to lowercase.
    """
    return s.replace('-', '').lower()


def get_closest_genre(token_text, threshold=80):
    match, score = process.extractOne(token_text, GENRES_LIST)
    if score >= threshold:
        return match
    return None


def enhanced_parse_query(query, df_movies):
    """
    Enhanced NLP parsing using SpaCy's NER and fuzzy matching to extract genres, specific movie names, actors, and directors.
    """
    # Initialize lists to hold extracted entities
    genres = []
    specific_movies = []
    actors = []
    directors = []

    # Normalize the entire query
    query_normalized = normalize_string(query)
    query_clean = query.strip().rstrip('.!?')

    # Use SpaCy for NER
    doc = nlp(query_clean)

    # Preprocess: create sets for titles, actors, directors for fast lookup
    # Normalize movie titles by removing hyphens and lowercasing
    movie_titles_normalized = set(normalize_string(title) for title in df_movies['title'].str.lower())

    # Use regex to split actors and directors by comma, 'and', or '&'
    split_pattern = r',|\band\b|\&'

    # Split and normalize director names, filtering out empty strings
    director_names = re.split(split_pattern, ', '.join(df_movies['directors'].dropna()))
    director_names = [name.strip() for name in director_names if name.strip()]
    director_names_normalized = set(normalize_string(name) for name in director_names)

    # Split and normalize actor names, filtering out empty strings
    actor_names = re.split(split_pattern, ', '.join(df_movies['actors'].dropna()))
    actor_names = [name.strip() for name in actor_names if name.strip()]
    actor_names_normalized = set(normalize_string(name) for name in actor_names)

    # Extract entities recognized by SpaCy
    for ent in doc.ents:
        ent_text_normalized = normalize_string(ent.text)

        # Check if the entity is a movie title
        if ent_text_normalized in movie_titles_normalized:
            # Find the actual title with proper casing
            original_title = df_movies[df_movies['title'].str.lower() == ent.text.lower()].iloc[0]['title']
            specific_movies.append(original_title)

        # Check if the entity is a director
        if ent_text_normalized in director_names_normalized:
            # Find the actual name with proper casing
            original_director = next((name for name in director_names if normalize_string(name) == ent_text_normalized),
                                     None)
            if original_director and original_director not in directors:
                directors.append(original_director)

        # Check if the entity is an actor
        if ent_text_normalized in actor_names_normalized:
            # Find the actual name with proper casing
            original_actor = next((name for name in actor_names if normalize_string(name) == ent_text_normalized), None)
            if original_actor and original_actor not in actors:
                actors.append(original_actor)

    # Secondary matching: Find actors, directors, and movies in the query even if SpaCy missed them
    # This ensures that entities like "tom hardy" are detected regardless of casing or hyphens
    if not actors:
        for actor_normalized in actor_names_normalized:
            if actor_normalized in query_normalized:
                # Find the actual name with proper casing
                original_actor = next((name for name in actor_names if normalize_string(name) == actor_normalized),
                                      None)
                if original_actor and original_actor not in actors:
                    actors.append(original_actor)

    if not directors:
        for director_normalized in director_names_normalized:
            if director_normalized in query_normalized:
                # Find the actual name with proper casing
                original_director = next(
                    (name for name in director_names if normalize_string(name) == director_normalized), None)
                if original_director and original_director not in directors:
                    directors.append(original_director)

    if not specific_movies:
        for movie_normalized in movie_titles_normalized:
            if movie_normalized in query_normalized:
                # Find the actual title with proper casing
                actual_title = \
                df_movies[df_movies['title'].str.lower().apply(normalize_string) == movie_normalized].iloc[0]['title']
                if actual_title not in specific_movies:
                    specific_movies.append(actual_title)

    # Additionally, perform exact and fuzzy matching for movie titles in the query
    # This helps in cases where SpaCy fails to recognize the movie title as an entity
    words = [token.text for token in doc]
    phrase = ' '.join(words)
    phrase_normalized = normalize_string(phrase)

    # Exact match
    exact_matches = df_movies[df_movies['title'].str.lower().apply(normalize_string).isin([phrase_normalized])]
    for title in exact_matches['title'].tolist():
        if title not in specific_movies:
            specific_movies.append(title)

    # Fuzzy match (threshold can be adjusted)
    fuzzy_matches = process.extract(phrase_normalized, movie_titles_normalized, limit=1)
    for match, score in fuzzy_matches:
        if score >= 90:
            # Find the actual title with proper casing
            actual_title = df_movies[df_movies['title'].str.lower().apply(normalize_string) == match].iloc[0]['title']
            if actual_title not in specific_movies:
                specific_movies.append(actual_title)

    # Extract genres based on predefined list with genre_variations
    for token in doc:
        if token.is_stop or token.is_punct or token.like_num or len(token.text) < 3:
            continue  # Skip unwanted tokens
        if token.pos_ not in ['ADJ', 'NOUN']:
            continue  # Only consider adjectives and nouns

        lemma = token.lemma_.lower()
        if lemma in GENRES_LIST:
            genres.append(lemma)
        elif token.text.lower() in GENRE_VARIATIONS:
            mapped_genre = GENRE_VARIATIONS[token.text.lower()]
            genres.append(mapped_genre)
        else:
            # Apply fuzzy matching
            closest_genre = get_closest_genre(token.text.lower())
            if closest_genre:
                genres.append(closest_genre)

    # Remove duplicates
    genres = list(set(genres))
    specific_movies = list(set(specific_movies))
    actors = list(set(actors))
    directors = list(set(directors))

    parsed = {
        'genres': genres,
        'specific_movies': specific_movies,
        'actors': actors,
        'directors': directors
    }

    # Log the parsed result for debugging
    logger.debug(f"Parsed Query: {parsed}")

    return parsed
