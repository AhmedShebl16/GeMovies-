# nancy/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .nlp_utils import enhanced_parse_query
from .recommendation import generate_recommendations
from .models import Movie, RecommendationRequest
from .serializers import (
    MovieSerializer,
    RecommendationRequestSerializer,
    RecommendationResponseSerializer
)
import pandas as pd
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RecommendMoviesView(generics.GenericAPIView):
    """
    API endpoint to receive user queries and return movie recommendations.
    """
    serializer_class = RecommendationRequestSerializer  # Link the request serializer

    # Define request body example
    request_body_example = {
        "application/json": {
            "query": "hey nancy give me some movies like Spider-Man",
            "limit": 10
        }
    }

    # Define response examples
    response_examples = {
        "200": {
            "query": "hey nancy give me some movies like Spider-Man",
            "limit": 10,
            "parsed": {
                "genres": ["romantic"],
                "specific_movies": ["Spider-Man"],
                "actors": [],
                "directors": []
            },
            "recommendations": [
                "Spider-Man 3",
                "Spider-Man: No Way Home",
                "Spider-Man: Into the Spider-Verse",
                "Spider-Man: Far From Home",
                "Spider-Man: Homecoming",
                "Spider-Man: Across the Spider-Verse",
                "Spider-Man: Beyond the Spider-Verse",
                "The Amazing Spider-Man",
                "The Amazing Spider-Man 2",
                "Spider-Man"
            ]
        },
        "400": {
            "query": ["This field is required."]
        },
        "404": {
            "detail": "No recommendations found based on your query."
        }
    }

    @swagger_auto_schema(
        request_body=RecommendationRequestSerializer,
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=RecommendationResponseSerializer,
                examples={
                    "application/json": response_examples["200"]
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": response_examples["400"]
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": response_examples["404"]
                }
            ),
        },
        operation_description="Receive a user query and return movie recommendations.",
        operation_summary="Recommend Movies",
        examples=request_body_example
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data.get('query', '')
        limit = serializer.validated_data.get('limit', 10)

        # Load movies DataFrame from the database
        movies_qs = Movie.objects.all()
        movies_data = list(movies_qs.values())
        df_movies = pd.DataFrame(movies_data)

        # Parse the query
        parsed = enhanced_parse_query(query, df_movies)

        # Check if any entities were parsed
        if not any([parsed['genres'], parsed['specific_movies'], parsed['actors'], parsed['directors']]):
            return Response(
                {"detail": "No recognizable genres, movies, actors, or directors found in the query."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate recommendations
        recommendations = generate_recommendations(parsed)

        # Check if any recommendations were found
        if not recommendations:
            return Response(
                {"detail": "No recommendations found based on your query."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Limit the number of recommendations
        recommendations = recommendations[:limit]

        # Log the recommendation request
        RecommendationRequest.objects.create(
            query=query,
            limit=limit,
            recommendations=', '.join(recommendations)
        )

        response_data = {
            "query": query,
            "limit": limit,
            "parsed": parsed,
            "recommendations": recommendations
        }

        response_serializer = RecommendationResponseSerializer(response_data)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class MovieListView(generics.ListAPIView):
    """
    API endpoint to list all movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer  # Link the serializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all movies.",
        operation_summary="List Movies",
        responses={200: MovieSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
