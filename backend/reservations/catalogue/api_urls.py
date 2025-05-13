# backend/reservations/catalogue/api_urls.py
from django.urls import path
# import absolu depuis la racine du projet DJango
from api.catalogue.views import (
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView
)

urlpatterns = [
    path('',     ArtistListCreateView.as_view(),              name='artist-list'),
    path('<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),
]
