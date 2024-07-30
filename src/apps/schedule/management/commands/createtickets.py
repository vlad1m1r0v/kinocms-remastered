import random
from django.core.management import BaseCommand

from apps.schedule.models import Ticket, Schedule
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Create Tickets"

    def handle(self, *args, **options):
        Ticket.objects.all().delete()

        tickets = []

        sessions = Schedule.objects.all()
        customer = CustomUser.objects.all().first()

        for session in sessions.iterator():
            hall = session.hall
            seats = list(hall.seats.all())
            n = random.randint(0, 100)

            random_seats = random.sample(seats, n)

            for seat in random_seats:
                tickets.append(Ticket(session=session, customer=customer, seat=seat))

        Ticket.objects.bulk_create(tickets)

        self.stdout.write(self.style.SUCCESS("Tickets were created successfully"))
