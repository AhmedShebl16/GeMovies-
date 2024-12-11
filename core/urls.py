# core/urls.py

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularJSONAPIView,
    SpectacularYAMLAPIView
)

# drf-spectacular URL patterns
dcos_patterns = [
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/yaml/', SpectacularYAMLAPIView.as_view(), name='schema_yaml_view'),
    path('api/docs/schema/json/', SpectacularJSONAPIView.as_view(), name='schema_json_view'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(), name='redoc_docs_view'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(), name='swagger_docs_view'),
]

# Application-specific URL patterns
apps_patterns = [
    path('api/accounts/', include('accounts.api.urls'), name='accounts'),
    path('api/profiles/', include('profiles.api.urls'), name='profiles'),  # Corrected path
    path('api/info/', include('info.urls'), name='info'),
    path('api/nancy/', include('nancy.urls'), name='nancy'),
    path('api/stats/', include('stats.api.urls'), name='stats'),
]

# All Project URL patterns
urlpatterns = [
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    *dcos_patterns,
    *apps_patterns
]

# Serve static and media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
