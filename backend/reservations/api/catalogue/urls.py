from django.urls import path
from .views import (
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView,
    ShowListView,
    UserProfileView
)

urlpatterns = [
    path('artists/', ArtistListCreateView.as_view(), name='api-artists-list'),
    path('artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='api-artists-detail'),
    path('shows/', ShowListView.as_view(), name='api-shows-list'),
     path("user/", UserProfileView.as_view(), name="api-user-profile"),
]
