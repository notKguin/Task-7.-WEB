from django.contrib import admin
from .models import Event, VolunteerApplication, Like


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "location", "starts_at", "ends_at", "created_at", "updated_at")
    search_fields = ("title", "location")
    list_filter = ("location", "starts_at")


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "status", "created_at", "updated_at")
    search_fields = ("user__email", "event__title")
    list_filter = ("status", "created_at")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "created_at")
    search_fields = ("user__email", "event__title")
