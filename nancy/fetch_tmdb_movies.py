# nancy/fetch_tmdb_movies.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def search_movies(query, page=1):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'page': page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_popular_movies(page=1):
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'page': page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_movie_details(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
