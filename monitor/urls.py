from django.urls import path
from . import views

urlpatterns = [
    path("section/<str:section>/", views.SectionView.as_view(),      name="section"),
    path("wave/",                  views.WaveChunkView.as_view(),    name="wave"),
    path("dashboard/",             views.DashboardView.as_view(),    name="dashboard"),  # changed from /snapshot to /dashboard
] 
