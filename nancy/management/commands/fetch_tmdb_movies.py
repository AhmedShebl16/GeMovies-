# nancy/management/commands/fetch_tmdb_movies.py
import requests
import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm
from nancy.models import Movie
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fetch movies from TMDB API and store them in the database.'

    def handle(self, *args, **kwargs):
        TMDB_API_KEY = os.getenv('TMDB_API_KEY')
        if not TMDB_API_KEY:
            self.stdout.write(self.style.ERROR("TMDB_API_KEY not found in environment variables."))
            return

        def get_genre_mapping(api_key):
            url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch genres: {response.status_code}")
            genres = response.json()['genres']
            genre_mapping = {genre['id']: genre['name'] for genre in genres}
            return genre_mapping

        def get_movie_details(api_key, movie_id):
            url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US'
            response = requests.get(url)
            if response.status_code != 200:
                self.stdout.write(self.style.WARNING(f"Failed to fetch credits for movie ID {movie_id}: {response.status_code}"))
                return {'directors': [], 'actors': []}
            data = response.json()
            directors = [member['name'] for member in data.get('crew', []) if member['job'] == 'Director']
            actors = [member['name'] for member in data.get('cast', [])[:5]]
            return {'directors': directors, 'actors': actors}

        def fetch_movies(api_key, total_pages=100):
            movies = []
            genre_mapping = get_genre_mapping(api_key)
            for page in tqdm(range(1, total_pages + 1), desc="Fetching movies"):
                url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page={page}'
                response = requests.get(url)
                if response.status_code != 200:
                    self.stdout.write(self.style.WARNING(f"Failed to fetch movies on page {page}: {response.status_code}"))
                    continue
                data = response.json()
                for movie in data.get('results', []):
                    movie_id = movie['id']
                    title = movie['title']
                    description = movie['overview']
                    genre_ids = movie['genre_ids']
                    genres = ', '.join([genre_mapping.get(gid, '') for gid in genre_ids])

                    details = get_movie_details(api_key, movie_id)
                    actors = ', '.join(details.get('actors', []))
                    directors = ', '.join(details.get('directors', []))

                    movies.append({
                        'title': title,
                        'description': description,
                        'genres': genres,
                        'actors': actors,
                        'directors': directors
                    })
            return pd.DataFrame(movies)

        df_movies = fetch_movies(TMDB_API_KEY, total_pages=100)
        self.stdout.write(self.style.SUCCESS(f"Fetched {df_movies.shape[0]} movies."))

        # Fetch existing titles from the database
        existing_titles = set(Movie.objects.values_list('title', flat=True).iterator())
        # Filter out movies that already exist
        new_movies_df = df_movies[~df_movies['title'].isin(existing_titles)]

        if new_movies_df.empty:
            self.stdout.write(self.style.WARNING("No new movies to add."))
            return

        # Create Movie instances
        movies_to_create = [
            Movie(
                title=row['title'],
                description=row['description'],
                genres=row['genres'],
                actors=row['actors'],
                directors=row['directors']
            )
            for _, row in new_movies_df.iterrows()
        ]

        # Bulk create
        Movie.objects.bulk_create(movies_to_create)
        self.stdout.write(self.style.SUCCESS(f"Added {len(movies_to_create)} new movies to the database."))
