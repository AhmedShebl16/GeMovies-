from django.urls import path
from info.views import MoviesListCreateView, MoviesRetrieveUpdateDestroyView

app_name = 'info'

urlpatterns = [
    path('movies/', MoviesListCreateView.as_view(), name='movies-list-create'),
    path('movies/<int:pk>/', MoviesRetrieveUpdateDestroyView.as_view(), name='movies-detail'),
]
