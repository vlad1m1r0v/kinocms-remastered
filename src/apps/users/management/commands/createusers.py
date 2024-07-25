from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
import datetime


class Command(BaseCommand):
    help = "Create User for Website and Superuser for Admin panel"

    def handle(self, *args, **options):
        # clear table
        CustomUser.objects.all().delete()

        # create user
        user = CustomUser.objects.create_user(
            nick_name="JSmith",
            email="email@spacelab.com",
            password="password",
            first_name="James",
            last_name="Smith",
            city="New York",
            address="123 Willow Creek Lane, Fairview, New York 12345, USA",
            card_number="1234123412341234",
            phone="+3800955555555",
            birth_date=datetime.date(2002, 5, 25),
            language="EN",
            sex="MALE",
        )

        # create superuser
        superuser = CustomUser.objects.create_superuser(
            nick_name="Admin",
            email="mypochtav@gmail.com",
            password="spacelab",
            first_name="Artem",
            last_name="Vladimirov",
            city="Kyiv",
            address="Apartment 12-B, Mykoly Pymonenka Street, Kyiv, Ukraine, 02000",
            card_number="4321432143214321",
            phone="+3800966666666",
            birth_date=datetime.date(2001, 4, 24),
            language="UK",
            sex="MALE",
            is_staff=True,
            is_superuser=True,
        )

        user.save()
        superuser.save()

        self.stdout.write(
            self.style.SUCCESS("User and Superuser were created successfully")
        )
