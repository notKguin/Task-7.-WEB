from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import EventViewSet, ApplicationViewSet, LikeViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"applications", ApplicationViewSet, basename="applications")
router.register(r"likes", LikeViewSet, basename="likes")

urlpatterns = [
    path("", include(router.urls)),
]
