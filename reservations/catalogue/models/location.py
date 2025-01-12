from django.db import models
from .locality import *

class LocationManager(models.Manager):
    def get_by_natural_key(self, slug, website):
        return self.get(slug=slug, website=website)

class Location(models.Model):
    slug = models.CharField(max_length=60, unique=True)
    designation = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    locality = models.ForeignKey(Locality, 
        on_delete=models.RESTRICT, null=True, related_name='locations')
    website = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=30, null=True)

    objects = LocationManager()

    def __str__(self):
        return self.designation

    class Meta:
        db_table = "locations"
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "website"],
                name="unique_slug_website",
            ),
        ]
    
    def natural_key(self):
        return (self.slug, self.website)
