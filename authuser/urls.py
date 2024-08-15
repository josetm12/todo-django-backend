# authuser/urls.py
from django.urls import path
from .views import (
    CreateUserView,
    LoginView,
    CheckAuthView,
    LogoutView,
    UpdateUserView,
    GetCSRFToken,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("check-auth/", CheckAuthView.as_view(), name="check-auth"),
    path("update/", UpdateUserView.as_view(), name="update"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("get-csrf-token/", GetCSRFToken.as_view(), name="get-csrf-token"),
]
