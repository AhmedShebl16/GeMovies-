# nancy/management/commands/fetch_tmdb_movies.py

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from nancy.models import Movie
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'Fetches popular movies from TMDB and loads them into the database.'

    def handle(self, *args, **options):
        api_key = settings.TMDB_API_KEY
        base_url = 'https://api.themoviedb.org/3/movie/popular'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json;charset=utf-8'
        }

        params = {
            'api_key': api_key,
            'language': 'en-US',
            'page': 1
        }

        total_pages = 1  # Initialize with 1 to enter the loop
        current_page = 1
        movies_created = 0
        movies_updated = 0

        while current_page <= total_pages:
            self.stdout.write(f'Fetching page {current_page} of {total_pages}')
            response = requests.get(base_url, params=params)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'Failed to fetch data: {response.status_code}'))
                break

            data = response.json()
            total_pages = data.get('total_pages', 1)
            results = data.get('results', [])

            for movie_data in results:
                tmdb_id = movie_data.get('id')
                movie_title = movie_data.get('title')
                overview = movie_data.get('overview', '')
                genre_ids = movie_data.get('genre_ids', [])
                release_date_str = movie_data.get('release_date', '')
                vote_average = movie_data.get('vote_average', 0.0)
                vote_count = movie_data.get('vote_count', 0)
                poster_path = movie_data.get('poster_path', '')
                backdrop_path = movie_data.get('backdrop_path', '')

                # Convert release_date to date object
                try:
                    release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                except ValueError:
                    release_date = None

                # Fetch additional movie details for runtime and director
                movie_details_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
                credits_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/credits'

                details_params = {
                    'api_key': api_key,
                    'language': 'en-US'
                }

                credits_params = {
                    'api_key': api_key,
                    'language': 'en-US'
                }

                # Fetch movie details
                details_response = requests.get(movie_details_url, params=details_params)
                if details_response.status_code == 200:
                    details = details_response.json()
                    runtime = details.get('runtime', 0)
                else:
                    runtime = 0
                    self.stdout.write(self.style.WARNING(f'Row: {movie_title} - Failed to fetch runtime.'))

                # Fetch movie credits to get director's name
                credits_response = requests.get(credits_url, params=credits_params)
                director_name = ''
                if credits_response.status_code == 200:
                    credits = credits_response.json()
                    crew = credits.get('crew', [])
                    directors = [member['name'] for member in crew if member['job'] == 'Director']
                    if directors:
                        director_name = ', '.join(directors)
                else:
                    self.stdout.write(self.style.WARNING(f'Row: {movie_title} - Failed to fetch credits.'))

                # Fetch genre names using genre IDs
                genres = self.get_genre_names(genre_ids, api_key)

                # Update or create the movie
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        'movie_title': movie_title,
                        'overview': overview,
                        'genres': genres,
                        'release_date': release_date,
                        'runtime_minutes': runtime if runtime else 0,
                        'director_name': director_name,
                        'movie_averageRating': vote_average,
                        'movie_numerOfVotes': vote_count,
                        'poster_path': poster_path,
                        'backdrop_path': backdrop_path,
                        # Add any additional fields here
                    }
                )

                if created:
                    movies_created += 1
                    self.stdout.write(self.style.SUCCESS(f'Created movie: {movie_title}'))
                else:
                    movies_updated += 1
                    self.stdout.write(self.style.WARNING(f'Updated movie: {movie_title}'))

                # To respect TMDB's rate limits
                time.sleep(0.25)  # Sleep for 250ms between requests

            current_page += 1
            params['page'] = current_page

            # To respect TMDB's rate limits
            time.sleep(0.25)  # Sleep for 250ms between page requests

        self.stdout.write(self.style.SUCCESS(f'Finished fetching movies. Created: {movies_created}, Updated: {movies_updated}'))

    def get_genre_names(self, genre_ids, api_key):
        """Fetches genre names based on genre IDs."""
        genres_url = 'https://api.themoviedb.org/3/genre/movie/list'
        params = {
            'api_key': api_key,
            'language': 'en-US'
        }
        response = requests.get(genres_url, params=params)
        if response.status_code == 200:
            genres_data = response.json()
            genres_list = genres_data.get('genres', [])
            genre_map = {genre['id']: genre['name'] for genre in genres_list}
            genre_names = [genre_map.get(genre_id, '') for genre_id in genre_ids]
            return ','.join(genre_names)
        else:
            self.stdout.write(self.style.WARNING('Failed to fetch genres.'))
            return ''
