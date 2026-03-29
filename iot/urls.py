from django.urls import path
from . import views

urlpatterns = [
    path("ingest/",       views.IoTIngestView.as_view(),     name="iot-ingest"),
    path("ingest/bulk/",  views.IoTBulkIngestView.as_view(), name="iot-bulk"),
    path("health/",       views.IoTHealthView.as_view(),     name="iot-health"),
]
