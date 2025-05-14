# backend/reservations/api/profile.py

from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # adapte les champs selon ton modèle
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Renvoie les informations de l'utilisateur connecté.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
