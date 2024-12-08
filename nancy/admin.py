# nancy/admin.py

from django.contrib import admin
from .models import MovieQuery

@admin.register(MovieQuery)
class MovieQueryAdmin(admin.ModelAdmin):
    list_display = ('query_snippet', 'created_at')
    search_fields = ('query',)
    list_filter = ('created_at',)
