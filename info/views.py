# info/views.py
from rest_framework import generics
from .models import Movies
from info.serializers import MoviesSerializer
from info.filters import MoviesFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class MoviesListCreateView(generics.ListCreateAPIView):
    """
    API view to list all movies and create a new movie.
    """
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MoviesFilter
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Override create to ensure only the latest 10 movies are stored.
        If the limit exceeds 10, remove the oldest entries.
        """
        response = super().create(request, *args, **kwargs)
        if Movies.objects.count() > 10:
            excess = Movies.objects.count() - 10
            oldest_movies = Movies.objects.order_by('release_date')[:excess]
            oldest_movies.delete()
            logger.debug(f"Deleted {excess} oldest movies to maintain the limit of 10.")
        return response

class MoviesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific movie.
    """
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer
    permission_classes = [AllowAny]
