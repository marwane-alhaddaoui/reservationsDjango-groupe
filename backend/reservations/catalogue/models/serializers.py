from rest_framework import serializers
from .artist import Artist
from .show import Show

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'firstname', 'lastname']


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'poster_url', 'price', 'bookable']