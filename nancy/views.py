# nancy/views.py

import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .models import MovieQuery
from .serializers import (
    MovieRecommendationInputSerializer,
    MovieRecommendationOutputSerializer
)
from django.conf import settings
from .nlp_utils import parse_query
from django.core.cache import cache
import logging
import pickle
import os
from django.http import JsonResponse  # Import if needed

logger = logging.getLogger('nancy')

# Load the trained recommendation model
BASE_DIR = settings.BASE_DIR
MODEL_DIR = os.path.join(BASE_DIR, 'nancy', 'ml_models')

# Load the DataFrame
with open(os.path.join(MODEL_DIR, 'df_movies.pkl'), 'rb') as f:
    df_movies = pickle.load(f)

# Load the indices mapping
with open(os.path.join(MODEL_DIR, 'indices.pkl'), 'rb') as f:
    indices = pickle.load(f)

# Load the TF-IDF Vectorizer
with open(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'), 'rb') as f:
    tfidf = pickle.load(f)

# Load the Cosine Similarity Matrix
with open(os.path.join(MODEL_DIR, 'cosine_sim.pkl'), 'rb') as f:
    cosine_sim = pickle.load(f)

# Define the recommendation function using the loaded models
def recommend_movies(title, cosine_sim=cosine_sim, indices=indices, df_movies=df_movies):
    title = title.lower()
    if title not in indices:
        logger.warning(f"Title '{title}' not found in indices.")
        return []
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar movies excluding itself
    movie_indices = [i[0] for i in sim_scores]
    similar_movies = df_movies['title'].iloc[movie_indices].tolist()
    return similar_movies

# Helper functions to fetch movies by genre, actor, director
def fetch_movies_by_genre(genre_name):
    genre_movies = df_movies[df_movies['genres'].str.contains(genre_name, case=False, na=False)]
    return genre_movies['title'].tolist()[:10]

def fetch_movies_by_actor(actor_name):
    actor_movies = df_movies[df_movies['actors'].str.contains(actor_name, case=False, na=False)]
    return actor_movies['title'].tolist()[:10]

def fetch_movies_by_director(director_name):
    director_movies = df_movies[df_movies['directors'].str.contains(director_name, case=False, na=False)]
    return director_movies['title'].tolist()[:10]

class RecommendMoviesView(APIView):
    @extend_schema(
        request=MovieRecommendationInputSerializer,
        responses={
            200: MovieRecommendationOutputSerializer,
            400: OpenApiResponse(description='Bad Request'),
            404: OpenApiResponse(description='No Recommendations Found'),
            500: OpenApiResponse(description='Internal Server Error'),
        },
        summary="Get Movie Recommendations from Nancy",
        description="Provide your movie preferences in natural language, and Nancy will recommend movies for you.",
        examples=[
            OpenApiExample(
                'Example 1',
                value={"query": "Hello Nancy, I would like to watch an action-packed thriller movie."},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                'Example 2',
                value={"query": "Hi Nancy, recommend me some romantic comedies."},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                'Example 3',
                value={"query": "Nancy, I'm in the mood for a horror movie directed by Wes Craven."},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                'Example 4',
                value={"query": "Nancy, suggest movies starring Leonardo DiCaprio."},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                'Example 5',
                value={"query": "Nancy, recommend some sci-fi movies similar to Interstellar."},
                request_only=True,
                response_only=False,
            ),
        ]
    )
    def post(self, request):
        input_serializer = MovieRecommendationInputSerializer(data=request.data)
        if input_serializer.is_valid():
            query_text = input_serializer.validated_data['query']
            parsed_data = parse_query(query_text)
            genres = parsed_data.get('genres', [])
            specific_movies = parsed_data.get('specific_movies', [])
            actors = parsed_data.get('actors', [])
            directors = parsed_data.get('directors', [])

            recommended = set()
            response_messages = []

            logger.info(f"Received query: {query_text}")
            logger.info(f"Parsed data: Genres={genres}, Specific Movies={specific_movies}, Actors={actors}, Directors={directors}")

            # Handle specific movie names using the trained model
            for movie in specific_movies:
                recommendations = recommend_movies(movie)
                if recommendations:
                    recommended.update(recommendations)
                    # Fetch movie details for better responses
                    movie_details = df_movies[df_movies['title'].str.lower() == movie.lower()]
                    if not movie_details.empty:
                        movie_desc = movie_details.iloc[0]['description'][:100]  # First 100 characters
                        response_messages.append(
                            f"Since you enjoyed **{movie}**, here are some similar movies you might like:\n"
                            + '\n'.join([f"- **{rec}**: {df_movies[df_movies['title'] == rec]['description'].values[0][:100]}..." for rec in recommendations[:3]])
                        )

            # Handle genres
            for genre in genres:
                genre_recommendations = fetch_movies_by_genre(genre)
                if genre_recommendations:
                    recommended.update(genre_recommendations)
                    response_messages.append(
                        f"For the **{genre}** genre, you might enjoy:\n"
                        + '\n'.join([f"- **{rec}**: {df_movies[df_movies['title'] == rec]['description'].values[0][:100]}..." for rec in genre_recommendations[:3]])
                    )

            # Handle actors
            for actor in actors:
                actor_recommendations = fetch_movies_by_actor(actor)
                if actor_recommendations:
                    recommended.update(actor_recommendations)
                    response_messages.append(
                        f"Movies starring **{actor}** that you might like:\n"
                        + '\n'.join([f"- **{rec}**: {df_movies[df_movies['title'] == rec]['description'].values[0][:100]}..." for rec in actor_recommendations[:3]])
                    )

            # Handle directors
            for director in directors:
                director_recommendations = fetch_movies_by_director(director)
                if director_recommendations:
                    recommended.update(director_recommendations)
                    response_messages.append(
                        f"Movies directed by **{director}** that you might enjoy:\n"
                        + '\n'.join([f"- **{rec}**: {df_movies[df_movies['title'] == rec]['description'].values[0][:100]}..." for rec in director_recommendations[:3]])
                    )

            # If no recommendations found
            if not recommended:
                logger.warning(f"No recommendations found for query: {query_text}")
                return Response(
                    {'response': "I couldn't find any recommendations based on your query. Could you please try asking differently?"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Limit to top 10 unique recommendations
            recommended = list(recommended)[:10]

            logger.info(f"Recommendations: {recommended}")

            # Save the query and recommendations to the database
            MovieQuery.objects.create(
                query=query_text,
                recommended_movies=', '.join(recommended)
            )

            # Prepare and return the response
            output_data = {
                'response': '\n\n'.join(response_messages),
                'recommended_movies': recommended
            }
            output_serializer = MovieRecommendationOutputSerializer(output_data)
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatView(APIView):
    """
    Since you're integrating with React, the chat interface will be handled on the frontend.
    This view can be repurposed or removed as needed.
    """
    # If you need authentication, uncomment the following line
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Chat interface is handled via the frontend. Use the /recommend/ endpoint for recommendations."}, status=status.HTTP_200_OK)
