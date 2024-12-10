# nancy/serializers.py
from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'actors', 'directors']

class RecommendationRequestSerializer(serializers.Serializer):
    query = serializers.CharField(
        required=True,
        help_text="User query for movie recommendations. Example: 'Hey Nancy, recommend some movies for Tom Hanks.'"
    )
    limit = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        help_text="Number of recommendations to return. Defaults to 10."
    )

class RecommendationResponseSerializer(serializers.Serializer):
    query = serializers.CharField()
    limit = serializers.IntegerField()
    parsed = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )
    recommendations = serializers.ListField(child=serializers.CharField())
