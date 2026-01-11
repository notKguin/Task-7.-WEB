from rest_framework import serializers
from .models import Event, VolunteerApplication, Like

class EventSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ("id", "title", "description", "location", "starts_at", "ends_at", "created_at", "updated_at", "likes_count")


class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = ("id", "user", "event", "motivation", "status", "created_at", "updated_at")
        read_only_fields = ("user", "status")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "event", "created_at", "updated_at")
        read_only_fields = ("user",)
