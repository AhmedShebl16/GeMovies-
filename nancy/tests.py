# nancy/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Movie

class RecommendMoviesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('recommend-movies')
        self.valid_payload = {
            "query": "I'm looking for a thrilling action movie."
        }
        self.invalid_payload = {
            "query": ""
        }

        # Create sample Movie instances
        Movie.objects.create(
            title="Thrilling Action Movie 1",
            description="An action-packed thriller.",
            genres="thriller, action",
            actors="Actor A, Actor B",
            directors="Director X"
        )
        Movie.objects.create(
            title="Thrilling Action Movie 2",
            description="Another thrilling action film.",
            genres="thriller, action",
            actors="Actor C, Actor D",
            directors="Director Y"
        )

    def test_recommend_movies_valid_payload(self):
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('recommendations', response.data)
        self.assertTrue(len(response.data['recommendations']) > 0)

    def test_recommend_movies_invalid_payload(self):
        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
