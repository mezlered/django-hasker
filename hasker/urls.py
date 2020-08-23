"""hasker URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('users.urls')),
    path('', include('questions.urls')),
    path('api/', include('api.urls',)),
    path('admin/', admin.site.urls),
]


if settings.DEBUG == True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )