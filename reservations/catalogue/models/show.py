from datetime import timedelta
from django.db import models
from .location import *
from django.urls import reverse
from django.utils.timezone import now

class ShowManager(models.Manager):
    def get_by_natural_key(self, slug, created_in):
        return self.get(slug=slug, created_in=created_in)

class Show(models.Model):
    slug = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True)
    poster_url = models.CharField(max_length=255, null=True)
    duration = models.PositiveSmallIntegerField(null=True)
    created_in = models.PositiveSmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shows')
    bookable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        # Vérifier si la date est dans moins de 30 minutes
        if self.schedule <= now() + timedelta(minutes=30):
            self.bookable = False
        super().save(*args, **kwargs)

    artist_types = models.ManyToManyField(
        "ArtistType",
        through="ArtistTypeShow",
        related_name="shows",
    )

    prices = models.ManyToManyField(
        "Price",
        through="ShowPrice",
        related_name="shows",
    )

    objects = ShowManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shows"
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "created_in"],
                name="unique_slug_created_in",
            ),
        ]

    def natural_key(self):
        return (self.slug, self.created_in)
    
    def get_absolute_url(self):
        return reverse('show_detail', kwargs={'slug': self.slug, 'created_in': self.created_in})

   


