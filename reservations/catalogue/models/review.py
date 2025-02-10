from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='reviews')
    show = models.ForeignKey('Show', on_delete=models.RESTRICT, related_name='reviews')
    review = models.TextField(blank=True, null=True)
    stars = models.PositiveSmallIntegerField()
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.show} - {self.stars} stars"

    class Meta:
        db_table = 'reviews'

#TODO: to implement Review model using the custom User Model -> uncomment the following code

# class Review(models.Model):
#     user = models.ForeignKey('User', on_delete=models.RESTRICT, related_name='reviews')
#     show = models.ForeignKey('Show', on_delete=models.RESTRICT, related_name='reviews')
#     review = models.TextField(blank=True, null=True)
#     stars = models.PositiveSmallIntegerField()
#     validated = models.BooleanField(default=False)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     def __str__(self):
#         return f"Review {self.id} - {self.stars} stars"

#     class Meta:
#         db_table = 'reviews'