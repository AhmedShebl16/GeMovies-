# nancy/management/commands/load_movies.py

import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from nancy.models import Movie
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Load movies from movie_statistic_dataset.csv'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'movie_statistic_dataset.csv')
        self.stdout.write(f'Loading movies from {file_path}')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, encoding='utf-8') as csvfile:
            # Determine the correct delimiter based on your CSV file
            # Change to '\t' if your CSV is tab-separated
            reader = csv.DictReader(csvfile, delimiter=',')  # Adjust delimiter if needed
            movies_created = 0
            movies_updated = 0
            for row_number, row in enumerate(reader, start=1):
                # Parse production_date
                try:
                    production_date = datetime.strptime(row['production_date'], '%m/%d/%Y').date()
                except (ValueError, TypeError):
                    production_date = None

                # Handle empty fields and non-integer values
                director_name = row['director_name'] if row['director_name'] != '-' else None
                director_professions = row['director_professions'] if row['director_professions'] != '-' else None

                # Safely parse integer fields
                def parse_int(value):
                    try:
                        return int(value)
                    except (ValueError, TypeError):
                        return None

                director_birthYear = parse_int(row['director_birthYear']) if row['director_birthYear'] not in [None, '-', ''] else None
                director_deathYear = parse_int(row['director_deathYear']) if row['director_deathYear'] not in [None, '-', ''] else None
                runtime_minutes = parse_int(row['runtime_minutes']) if row['runtime_minutes'] not in [None, '-', ''] else 0
                movie_averageRating = float(row['movie_averageRating']) if row['movie_averageRating'] not in [None, '-', ''] else 0.0
                movie_numerOfVotes = parse_int(row['movie_numerOfVotes']) if row['movie_numerOfVotes'] not in [None, '-', ''] else 0
                approval_Index = float(row['approval_Index']) if row['approval_Index'] not in [None, '-', ''] else 0.0
                production_budget = parse_int(row['Production budget $']) if row['Production budget $'] not in [None, '-', ''] else 0
                domestic_gross = parse_int(row['Domestic gross $']) if row['Domestic gross $'] not in [None, '-', ''] else 0
                worldwide_gross = parse_int(row['Worldwide gross $']) if row['Worldwide gross $'] not in [None, '-', ''] else 0

                # Create or update Movie
                try:
                    movie, created = Movie.objects.update_or_create(
                        movie_title=row['movie_title'],
                        defaults={
                            'production_date': production_date,
                            'genres': row['genres'] if row['genres'] not in [None, '-', ''] else '',
                            'runtime_minutes': runtime_minutes,
                            'director_name': director_name,
                            'director_professions': director_professions,
                            'director_birthYear': director_birthYear,
                            'director_deathYear': director_deathYear,
                            'movie_averageRating': movie_averageRating,
                            'movie_numerOfVotes': movie_numerOfVotes,
                            'approval_Index': approval_Index,
                            'production_budget': production_budget,
                            'domestic_gross': domestic_gross,
                            'worldwide_gross': worldwide_gross,
                        }
                    )
                    if created:
                        movies_created += 1
                    else:
                        movies_updated += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing row {row_number}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {movies_created} new movies and updated {movies_updated} existing movies.'))
