from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# 🔐 Fonction utilitaire pour générer les tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Serializer pour l'inscription
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Vue d'inscription avec réponse incluant les tokens
class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ⬇️ Génération des tokens
        tokens = get_tokens_for_user(user)

        # ⬇️ Fusion des données utilisateur + tokens
        data = serializer.data
        data.update(tokens)

        return Response(data, status=status.HTTP_201_CREATED)
