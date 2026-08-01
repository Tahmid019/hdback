from django.urls import path, include
from .auth_views import CurrentUserView
from .jwt_utils import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("api/auth/login/",   CustomTokenObtainPairView.as_view(), name="auth-login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(),          name="auth-refresh"),
    path("api/auth/me/",      CurrentUserView.as_view(),           name="auth-me"),
    path("api/",              include("monitor.urls")),
    path("iot/",              include("iot.urls")),
]
