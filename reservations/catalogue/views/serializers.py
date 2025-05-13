from catalogue.models.artist import Artist
from rest_framework import serializers
from catalogue.models import Artist, ArtistType, Show


class ArtistTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.type')

    class Meta:
        model = ArtistType
        fields = ['type']

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'duration', 'bookable']

class ArtistSerializer(serializers.ModelSerializer):
    types = ArtistTypeSerializer(source='a_artistTypes', many=True)
    shows = ShowSerializer(many=True)  # Removed redundant 'source' argument

    class Meta:
        model = Artist
        fields = ['id', 'firstname', 'lastname', 'types', 'shows']