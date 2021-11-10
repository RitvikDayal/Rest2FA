from django.urls import path

from .views import (
    TOTPClientCreateView,
    TOTPVerifyView,
    ProtectView,
)

urlpatterns = [
    path(
        "2fa/registration/", TOTPClientCreateView.as_view(), name="totp-client-register"
    ),
    path("2fa/verify/<int:token>/", TOTPVerifyView.as_view(), name="totp-verify"),
    path("2fa/protected/", ProtectView.as_view(), name="totp-protect"),
]
