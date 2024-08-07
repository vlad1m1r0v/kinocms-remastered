from django.db import models

from apps.films.models import Film
from apps.halls.models import Hall, Seat
from apps.users.models import CustomUser


# Create your models here.
class Schedule(models.Model):
    time = models.DateTimeField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sessions')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    price = models.SmallIntegerField()


class Ticket(models.Model):
    session = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
