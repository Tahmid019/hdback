from django.urls import path, include

urlpatterns = [
    path("api/", include("monitor.urls")),
    path("iot/", include("iot.urls")),
]
