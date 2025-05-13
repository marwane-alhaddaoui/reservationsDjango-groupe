#TODO: Implement the User model -> uncomment the following code

# from django.db import models

# class User(models.Model):
#     login = models.CharField(max_length=30)
#     password = models.CharField(max_length=255)
#     firstname = models.CharField(max_length=60)
#     lastname = models.CharField(max_length=60)
#     email = models.EmailField()
#     langue = models.CharField(max_length=2, blank=True, null=True)

#     def __str__(self):
#         return self.login

#     class Meta:
#         db_table = 'users'