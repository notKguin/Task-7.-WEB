from django.urls import path
from .views import SignInView, SignOutView, register

urlpatterns = [
    path("login/", SignInView.as_view(), name="login"),
    path("logout/", SignOutView.as_view(), name="logout"),
    path("register/", register, name="register"),
]
