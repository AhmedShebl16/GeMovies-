from rest_framework import serializers
from .models import Movies

class MoviesSerializer(serializers.ModelSerializer):
    """
    Serializer for Movies model to handle serialization and deserialization.
    """
    class Meta:
        model = Movies
        fields = [
            'id', 'name', 'genre', 'rating', 'tmdb_id',
            'poster_path', 'overview', 'release_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
