from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Model
from typing import Type
from .models import Hall, Seat


@receiver(post_save, sender=Hall)
def create_seats(sender: Type[Model], instance: Hall, created: bool, **kwargs) -> None:
    if created:
        seats = []
        for row in range(1, 11):
            for column in range(1, 11):
                code = f"{row}{chr(64 + column)}"
                seats.append(Seat(hall=instance, row=row, column=column, code=code))
        Seat.objects.bulk_create(seats)
