from django.urls import path, include
from .auth_views import CurrentUserView

urlpatterns = [
    path("api/auth/me/", CurrentUserView.as_view(), name="auth-me"),
    path("api/", include("monitor.urls")),
    path("iot/", include("iot.urls")),
]
