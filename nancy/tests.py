# nancy/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import MovieQuery

class RecommendMoviesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('nancy:recommend_movies')
        self.valid_payload = {
            "query": "Nancy, recommend me some action movies starring Tom Cruise."
        }
        self.invalid_payload = {
            "query": ""
        }

    def test_recommend_movies_valid(self):
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('recommended_movies', response.data)
        self.assertIn('response', response.data)
        self.assertIsInstance(response.data['recommended_movies'], list)
        self.assertGreater(len(response.data['recommended_movies']), 0)

    def test_recommend_movies_invalid(self):
        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('query', response.data)

    def test_recommend_movies_no_recommendations(self):
        # Assuming "NonExistentMovie" is not in your dataset
        payload = {
            "query": "Nancy, recommend me some movies similar to NonExistentMovie."
        }
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('response', response.data)
