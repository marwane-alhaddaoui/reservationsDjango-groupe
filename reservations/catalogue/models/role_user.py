#TODO: Implement RoleUser model -> uncomment the following code

# from django.db import models

# class RoleUser(models.Model):
#     role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role_users')
#     user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='role_users')

#     def __str__(self):
#         return self.role.role + ' - ' + self.user.username
    
#     class Meta:
#         db_table = 'role_user'