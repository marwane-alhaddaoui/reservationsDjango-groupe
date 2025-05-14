from rest_framework import generics
from catalogue.models.show import Show
from catalogue.models.serializers import ShowSerializer
from rest_framework.permissions import AllowAny

class ShowListAPIView(generics.ListAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]
