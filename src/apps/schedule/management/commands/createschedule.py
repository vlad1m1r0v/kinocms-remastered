import random
from itertools import product
from datetime import datetime, timedelta
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from apps.films.models import Film
from apps.halls.models import Hall
from apps.schedule.models import Schedule


class Command(BaseCommand):
    help = "Create Schedule for a week ahead and a past week"

    def handle(self, *args, **options):
        # Delete all records first
        Schedule.objects.all().delete()

        films = Film.objects.all()
        halls = Hall.objects.all()

        # Define all possible Film-Hall combinations
        films_halls = [result for result in product(list(films), list(halls))]

        # Define time intervals
        days = [*range(-7, 8)]
        hours = [*range(18, 23)]
        minutes = [*range(0, 60, 15)]
        times = product(days, hours, minutes)

        base_date = datetime.now().date()
        show_times = [make_aware(datetime.combine(base_date + timedelta(days=days),
                                                  datetime
                                                  .strptime(f'{hours:02d}:{minutes:02d}', '%H:%M')
                                                  .time())) for (days, hours, minutes) in times]

        schedules = []

        for index, show_time in enumerate(show_times):
            (film, hall) = films_halls[index % len(films_halls)]
            price = random.choice([x for x in range(150, 251, 10)])
            schedule = Schedule(
                time=show_time,
                hall=hall,
                film=film,
                price=price
            )
            schedules.append(schedule)

        Schedule.objects.bulk_create(schedules)

        self.stdout.write(self.style.SUCCESS("Schedule was created successfully"))
