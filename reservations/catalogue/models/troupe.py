from django.db import models

class Troupe(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id de la troupe")
    name = models.CharField(max_length=60, unique=True, help_text="Nom de la troupe")
    logo_url = models.CharField(max_length=250, null=True, blank=True, help_text="URL du logo de la troupe")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "troupes"
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_troupe_name")
        ]
