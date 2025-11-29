from django.urls import path
from .views import TopTrackView

urlpatterns = [
    path('toptracks/', TopTrackView.as_view(), name="top_track_view")
]