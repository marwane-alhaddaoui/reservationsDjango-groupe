from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from catalogue.models.artist import Artist
from catalogue.models.troupe import Troupe

# Helper function to check if the user is staff
def is_staff_user(user):
    return user.is_staff

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_staff_user)
def manage_troupe(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        return Response({"error": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if artist.troupe:
            return Response({
                "troupe": {
                    "id": artist.troupe.id,
                    "name": artist.troupe.name,
                    "logo_url": artist.troupe.logo_url
                }
            })
        else:
            return Response({"message": "This artist does not belong to any troupe."})

    elif request.method == 'POST':
        troupe_id = request.data.get('troupe_id')
        if not troupe_id:
            return Response({"error": "Troupe ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            troupe = Troupe.objects.get(id=troupe_id)
        except Troupe.DoesNotExist:
            return Response({"error": "Troupe not found."}, status=status.HTTP_404_NOT_FOUND)

        artist.troupe = troupe
        artist.save()
        return Response({"message": "Troupe assigned successfully to the artist."})
