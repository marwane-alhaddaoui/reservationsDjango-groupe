from django.db import models

class RepresentationReservation(models.Model):
    representation = models.ForeignKey('Representation', on_delete=models.CASCADE, related_name='representation_reservations')
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='representation_reservations')
    price = models.ForeignKey('Price', on_delete=models.CASCADE, related_name='representation_reservations')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.representation.show.title + ' - ' + self.reservation.user.username + ' - ' + self.reservation.date.strftime('%d/%m/%Y %H:%M')
    
    class Meta:
        db_table = 'representation_reservation'