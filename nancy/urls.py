# nancy/urls.py

from django.urls import path
from .views import RecommendMoviesView, ChatView

urlpatterns = [
    path('recommend/', RecommendMoviesView.as_view(), name='recommend_movies'),
    path('chat/', ChatView.as_view(), name='nancy_chat'),
]
