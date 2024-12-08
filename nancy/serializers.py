# nancy/serializers.py

from rest_framework import serializers

class MovieRecommendationInputSerializer(serializers.Serializer):
    query = serializers.CharField(
        max_length=1000,
        help_text="Provide your movie preference in natural language."
    )

class MovieRecommendationOutputSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=5000, required=False)
    recommended_movies = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
