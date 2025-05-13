# backend/catalogue/api_urls.py
from django.urls import path
from ..api.catalogue.views import ArtistListAPIView  # à adapter selon ton projet

urlpatterns = [
    path('', ArtistListAPIView.as_view(), name='artist-list'),
]
