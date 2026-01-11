from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError

from .models import Event, VolunteerApplication, Like
from .serializers import EventSerializer, VolunteerApplicationSerializer, LikeSerializer


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return Event.objects.all().annotate(likes_count=Count("likes"))


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VolunteerApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        event = serializer.validated_data.get("event")
        if VolunteerApplication.objects.filter(user=self.request.user, event=event).exists():
            raise ValidationError({"detail": "Заявка на это мероприятие уже существует."})
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        event = serializer.validated_data.get("event")
        if Like.objects.filter(user=self.request.user, event=event).exists():
            raise ValidationError({"detail": "Лайк уже поставлен."})
        serializer.save(user=self.request.user)
