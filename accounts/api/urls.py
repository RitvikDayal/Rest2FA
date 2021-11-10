from django.urls import path, include

urlpatterns = [
    path("v1/", include("accounts.api.v1.urls")),
    path("v2/", include("accounts.api.v2.urls")),
]
