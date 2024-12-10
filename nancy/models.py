# nancy/models.py
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    actors = models.CharField(max_length=255, blank=True, null=True)
    directors = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class RecommendationRequest(models.Model):
    query = models.TextField()
    limit = models.PositiveIntegerField(default=10)
    recommendations = models.TextField()  # Store as comma-separated titles
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation Request at {self.timestamp}"
