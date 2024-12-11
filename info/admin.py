from django.contrib import admin
from .models import Movies

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    """
    Admin interface for Movies model.
    """
    list_display = ('name', 'genre', 'rating', 'release_date', 'created_at', 'updated_at')
    search_fields = ('name', 'genre')
    list_filter = ('genre', 'rating', 'release_date')
    readonly_fields = ('created_at', 'updated_at')
