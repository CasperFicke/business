# business/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  # admin urls
  path('admin/', admin.site.urls),
  # App urls
  path('', include('core.urls', namespace="core")),
  path('', include('users.urls', namespace="users")),
  # debug urls
  path("__debug__", include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)