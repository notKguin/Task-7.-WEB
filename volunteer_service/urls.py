from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from core.views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
