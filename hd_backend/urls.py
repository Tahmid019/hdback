from django.urls import include, path
from monitor.views import AuthCheckView 

urlpatterns = [
    path('api/auth-check/', AuthCheckView.as_view(), name='auth-check'),
    path("api/", include("monitor.urls")),
    path("iot/", include("iot.urls")),
]