from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegisterForm


class SignInView(LoginView):
    template_name = "accounts/login.html"


class SignOutView(LogoutView):
    next_page = reverse_lazy("events:list")


def register(request):
    if request.user.is_authenticated:
        return redirect("events:list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("events:list")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
