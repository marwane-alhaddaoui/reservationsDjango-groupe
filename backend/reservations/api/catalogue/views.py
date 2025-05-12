from catalogue.models.artist import Artist
from catalogue.models.show import Show
from catalogue.models.serializers import ArtistSerializer, ShowSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny


# ARTISTES

class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]  # accessible sans login

class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]


# SPECTACLES

class ShowListView(generics.ListAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]
