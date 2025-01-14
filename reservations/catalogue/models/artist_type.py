from django.db import models

class ArtisteType(models.Model):
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='artiste_types')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, related_name='artiste_types')

    def __str__(self):
        return self.artist.name + ' - ' + self.type.label
    
    class Meta:
        db_table = 'artiste_type'