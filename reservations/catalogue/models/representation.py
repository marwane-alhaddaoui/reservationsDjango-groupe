from django.db import models

class Representation(models.Model):
    show = models.ForeignKey('Show', on_delete=models.CASCADE, related_name='representations')
    schedule = models.DateTimeField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='representations')

    def __str__(self):
        return self.show.title + ' - ' + self.schedule.strftime('%d/%m/%Y %H:%M')
    
    class Meta:
        db_table = 'representations'