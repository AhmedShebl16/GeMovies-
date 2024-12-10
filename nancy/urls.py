# nancy/urls.py
from django.urls import path
from .views import RecommendMoviesView, MovieListView

urlpatterns = [
    path('recommend/', RecommendMoviesView.as_view(), name='recommend-movies'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
]
