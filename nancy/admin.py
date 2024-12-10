# nancy/admin.py
from django.contrib import admin
from .models import Movie, RecommendationRequest

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genres', 'actors', 'directors')
    search_fields = ('title', 'genres', 'actors', 'directors')
    list_filter = ('genres',)


@admin.register(RecommendationRequest)
class RecommendationRequestAdmin(admin.ModelAdmin):
    list_display = ('query', 'limit', 'short_recommendations', 'timestamp')
    search_fields = ('query', 'recommendations')
    list_filter = ('timestamp',)
    readonly_fields = ('query', 'limit', 'recommendations', 'timestamp')

    def short_recommendations(self, obj):
        recs = obj.recommendations.split(', ')
        if len(recs) > 3:
            return ', '.join(recs[:3]) + '...'
        return obj.recommendations
    short_recommendations.short_description = 'Recommendations'
