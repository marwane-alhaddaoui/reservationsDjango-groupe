from django.urls import path
from .views import (
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView,
    ShowListView
)

urlpatterns = [
    path('artists/', ArtistListCreateView.as_view(), name='api-artists-list'),
    path('artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='api-artists-detail'),
    path('shows/', ShowListView.as_view(), name='api-shows-list'),
]
