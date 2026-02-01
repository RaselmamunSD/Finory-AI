"""
URL configuration for finory_ia project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views.root_view import api_root
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Customize admin site
admin.site.site_header = 'Finory IA Administration'
admin.site.site_title = 'Finory IA Admin'
admin.site.index_title = 'Welcome to Finory IA Administration'

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    # OpenAPI schema and Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
