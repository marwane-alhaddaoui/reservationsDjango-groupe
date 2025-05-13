# backend/reservations/catalogue/api_urls.py

from django.urls import path
# import des classes correctes :
from ..api.catalogue.views import (
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView
)

urlpatterns = [
    # liste + création
    path('', ArtistListCreateView.as_view(), name='artist-list'),
    # détails / maj / suppression
    path('<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),
]
