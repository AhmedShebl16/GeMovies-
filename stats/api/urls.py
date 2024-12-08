from django.urls import path, include

from rest_framework import routers

from .views import UserStatsViewSet, ProfileStatsViewSet


app_name = 'stats'

router = routers.DefaultRouter()
router.register('users', UserStatsViewSet, basename='users')
router.register('profiles', ProfileStatsViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls), name='users'),
]
