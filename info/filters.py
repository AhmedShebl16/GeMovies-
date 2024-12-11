# info/filters.py
import django_filters
from .models import Movies

class MoviesFilter(django_filters.FilterSet):
    """
    FilterSet for Movies model to enable filtering based on name, genre, and rating.
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label="Movie Name Contains"
    )
    genre = django_filters.CharFilter(
        field_name='genre',
        lookup_expr='icontains',
        label="Genre Contains"
    )
    min_rating = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label="Minimum Rating"
    )
    max_rating = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='lte',
        label="Maximum Rating"
    )

    class Meta:
        model = Movies
        fields = ['name', 'genre', 'min_rating', 'max_rating']
