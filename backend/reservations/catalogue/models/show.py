from django.db import models
from .location import *

class ShowManager(models.Manager):
    def get_by_natural_key(self, slug, created_at):
        return self.get(slug=slug, created_at=created_at)


# Create your models here.
class Show(models.Model):
   slug = models.CharField(max_length=60, unique=True)
   title = models.CharField(max_length=255)
   description = models.TextField(max_length=255, null=True)  # Permet NULL
   poster_url = models.CharField(max_length=255, null=True)  # Permet NULL
   duration = models.PositiveSmallIntegerField(null=True)  # Permet NULL
   created_in = models.PositiveSmallIntegerField(null=True)  # Permet NULL
   location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shows')
   bookable = models.BooleanField(default=True, null=True)  # Permet NULL
   price = models.DecimalField(decimal_places=2, max_digits=10, null=True)  # Nouveau champ price
   created_at = models.DateTimeField(auto_now_add=True, null=True)  # Permet NULL
   updated_at = models.DateTimeField(auto_now=True, null=True)  # Permet NULL
artist_types = models.ManyToManyField(
        "ArtistType",
        through="ArtistTypeShow",
        related_name="shows",
    )

   
   
objects = ShowManager()
    
def __str__(self):
        return self.title
    
class Meta:
        db_table = "shows"
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "created_at"],
                name="unique_slug_created_at",
            ),
        ]

def natural_key(self):
        return (self.slug, self.created_at)
