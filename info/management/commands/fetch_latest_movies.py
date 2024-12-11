# info/management/commands/fetch_latest_movies.py
import requests
from django.core.management.base import BaseCommand, CommandError
from info.models import Movies
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch the latest 10 movies from TMDB and store them in the Movies model.'

    def handle(self, *args, **options):
        tmdb_api_key = settings.TMDB_API_KEY
        if not tmdb_api_key:
            raise CommandError("TMDB_API_KEY is not set in settings.py or environment variables.")

        url = f'https://api.themoviedb.org/3/movie/now_playing'
        params = {
            'api_key': tmdb_api_key,
            'language': 'en-US',
            'page': 1
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise CommandError(f"Failed to fetch movies from TMDB: {response.text}")

        data = response.json()
        movies = data.get('results', [])[:10]  # Get the first 10 movies

        for movie_data in movies:
            tmdb_id = movie_data.get('id')
            name = movie_data.get('title')
            genre_ids = movie_data.get('genre_ids', [])
            genres = self.get_genres(genre_ids)
            rating = movie_data.get('vote_average', 0)
            poster_path = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}" if movie_data.get('poster_path') else ''
            overview = movie_data.get('overview', '')
            release_date = movie_data.get('release_date', None)

            # Create or update the movie entry
            movie, created = Movies.objects.update_or_create(
                tmdb_id=tmdb_id,
                defaults={
                    'name': name,
                    'genre': genres,
                    'rating': rating,
                    'poster_path': poster_path,
                    'overview': overview,
                    'release_date': release_date
                }
            )
            if created:
                logger.info(f"Added new movie: {name}")
            else:
                logger.info(f"Updated movie: {name}")

        # Ensure only the latest 10 movies are kept
        all_movies = Movies.objects.all().order_by('-release_date')
        if all_movies.count() > 10:
            excess = all_movies.count() - 10
            movies_to_delete = all_movies[10:]
            for movie in movies_to_delete:
                logger.info(f"Deleting movie: {movie.name}")
            all_movies[10:].delete()

        self.stdout.write(self.style.SUCCESS('Successfully fetched and updated the latest 10 movies from TMDB.'))

    def get_genres(self, genre_ids):
        """
        Convert genre IDs to genre names using TMDB's genre list.
        """
        tmdb_api_key = settings.TMDB_API_KEY
        genre_url = f'https://api.themoviedb.org/3/genre/movie/list'
        params = {
            'api_key': tmdb_api_key,
            'language': 'en-US'
        }
        response = requests.get(genre_url, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to fetch genres from TMDB: {response.text}")
            return 'Unknown'

        genres_data = response.json().get('genres', [])
        genre_map = {genre['id']: genre['name'] for genre in genres_data}
        genres = [genre_map.get(genre_id, 'Unknown') for genre_id in genre_ids]
        return ', '.join(genres)
