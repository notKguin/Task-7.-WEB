from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Exists, OuterRef, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ApplicationForm
from .models import Event, VolunteerApplication, Like
from .services.xlsx_export import ExportService


def event_list(request: HttpRequest) -> HttpResponse:
    q = (request.GET.get("q") or "").strip()
    location = (request.GET.get("location") or "").strip()
    sort = (request.GET.get("sort") or "").strip()  # starts, -starts, likes

    events = Event.objects.all().annotate(
        likes_count=Count("likes", distinct=True),
    )

    if q:
        events = events.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if location:
        events = events.filter(location__icontains=location)

    if sort == "starts":
        events = events.order_by("starts_at")
    elif sort == "-starts":
        events = events.order_by("-starts_at")
    elif sort == "likes":
        events = events.order_by("-likes_count", "-starts_at")

    user_likes = set()
    if request.user.is_authenticated:
        user_likes = set(Like.objects.filter(user=request.user).values_list("event_id", flat=True))

    ctx = {
        "events": events,
        "q": q,
        "location": location,
        "sort": sort,
        "user_likes": user_likes,
    }
    return render(request, "core/event_list.html", ctx)


def event_detail(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event.objects.annotate(likes_count=Count("likes")), pk=pk)

    existing_app = None
    if request.user.is_authenticated:
        existing_app = VolunteerApplication.objects.filter(user=request.user, event=event).first()

    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, event=event).exists()

    return render(
        request,
        "core/event_detail.html",
        {"event": event, "existing_app": existing_app, "liked": liked},
    )


@login_required
def apply_event(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)

    if VolunteerApplication.objects.filter(user=request.user, event=event).exists():
        messages.info(request, "Вы уже подали заявку на это мероприятие.")
        return redirect("events:detail", pk=pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.event = event
            app.save()
            messages.success(request, "Заявка отправлена и ожидает рассмотрения.")
            return redirect("events:detail", pk=pk)
    else:
        form = ApplicationForm()

    return render(request, "core/apply.html", {"event": event, "form": form})


@login_required
def toggle_like(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("events:detail", pk=pk)

    event = get_object_or_404(Event, pk=pk)
    like = Like.objects.filter(user=request.user, event=event).first()
    if like:
        like.delete()
        messages.info(request, "Лайк убран.")
    else:
        Like.objects.create(user=request.user, event=event)
        messages.success(request, "Спасибо за поддержку!")
    return redirect(request.META.get("HTTP_REFERER") or reverse("events:detail", kwargs={"pk": pk}))


def is_staff(user) -> bool:
    return user.is_staff or user.is_superuser


@user_passes_test(is_staff)
def export_xlsx(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        model_key = request.POST.get("model") or ""
        fields = request.POST.getlist("fields") or []
        try:
            service = ExportService()
            content, filename = service.build_xlsx(model_key=model_key, fields=fields)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("events:export")

        resp = HttpResponse(
            content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp

    service = ExportService()
    return render(request, "core/export.html", {"models": service.get_models()})
