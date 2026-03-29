from django.urls import path
from . import views

urlpatterns = [
    path("snapshot/",        views.FullSnapshotView.as_view(),          name="snapshot"),
    path("section/<str:section>/", views.SectionView.as_view(),         name="section"),
    path("wave/",            views.WaveChunkView.as_view(),              name="wave"),
]
