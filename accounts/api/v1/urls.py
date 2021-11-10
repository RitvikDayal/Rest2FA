from django.urls import path
from .views import (
    UserLoginView,
    User2FARegistrationView,
    User2FAAuthenticationView,
    UserRegistrationView,
    LogoutHandlerView,
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("log-out/", LogoutHandlerView.as_view(), name="user_logout"),
    path(
        "2fa/registration/", User2FARegistrationView.as_view(), name="2fa_registration"
    ),
    path(
        "2fa/authentication/",
        User2FAAuthenticationView.as_view(),
        name="2fa_authentication",
    ),
]
