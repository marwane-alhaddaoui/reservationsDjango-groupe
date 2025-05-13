from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from catalogue.views.serializers import ArtistSerializer
from catalogue.models import Artist

@api_view(['GET'])
def artist_list(request):
    all_artists = request.query_params.get('all', 'false').lower() == 'true'
    if all_artists:
        artists = Artist.objects.all()
    else:
        paginator = PageNumberPagination()
        paginator.page_size = 30
        artists = paginator.paginate_queryset(Artist.objects.all(), request)
        return paginator.get_paginated_response([
            {"id": artist.id, "firstname": artist.firstname, "lastname": artist.lastname}
            for artist in artists
        ])
    return Response([
        {"id": artist.id, "firstname": artist.firstname, "lastname": artist.lastname}
        for artist in artists
    ])

class ArtistDetailView(APIView):
    def get(self, request, pk):
        try:
            artist = Artist.objects.prefetch_related('a_artistTypes__type', 'shows').get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Artist.DoesNotExist:
            return Response({"error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)