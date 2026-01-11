from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),
    path("events/<int:pk>/", views.event_detail, name="detail"),
    path("events/<int:pk>/apply/", views.apply_event, name="apply"),
    path("events/<int:pk>/like/", views.toggle_like, name="like"),

    path("admin-tools/export/", views.export_xlsx, name="export"),
]
