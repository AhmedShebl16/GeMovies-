# nancy/models.py

from django.db import models

class MovieQuery(models.Model):
    query = models.CharField(
        max_length=1000,
        help_text="User's natural language query.",
        null=True,
        blank=True
    )
    recommended_movies = models.TextField(
        help_text="Comma-separated list of recommended movies.",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query_snippet()

    def query_snippet(self):
        if self.query:
            return (self.query[:50] + '...') if len(self.query) > 50 else self.query
        return "No Query Provided"
