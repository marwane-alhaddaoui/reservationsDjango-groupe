from django.db import models
from .type import *
from django.http import JsonResponse
from .show import Show  


class ArtistManager(models.Manager):
    def get_by_natural_key(self, firstname, lastname):
        return self.get(firstname=firstname, lastname=lastname)

class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    shows = models.ManyToManyField(Show, related_name='artists', through='ArtistShow')  # Ajout de la relation Many-to-Many
    troupe = models.ForeignKey(
        "catalogue.Troupe",
        on_delete=models.PROTECT,  
        related_name="artists",
        null=True,  
        blank=True
    )
    

    objects = ArtistManager()

    def __str__(self):
        return self.firstname +" "+ self.lastname
    
    class Meta:
        db_table = "artists"
        constraints = [
            models.UniqueConstraint(
                fields=["firstname", "lastname"],
                name="unique_firstname_lastname",
            ),
        ]

    def natural_key(self):
        return (self.firstname, self.lastname)
    
    def save(self, *args, **kwargs):
        if not self.troupe:
            from catalogue.models.troupe import Troupe
            non_affilie, created = Troupe.objects.get_or_create(name="Non affilié")
            self.troupe = non_affilie
        super().save(*args, **kwargs)

def artist_list(request):
    artists = Artist.objects.all().values('id', 'firstname', 'lastname')
    return JsonResponse(list(Artist), safe=False)