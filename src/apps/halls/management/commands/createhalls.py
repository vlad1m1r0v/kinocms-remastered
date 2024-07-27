import os
import random
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.cinemas.models import Cinema
from apps.halls.models import Hall, HallImage


class Command(BaseCommand):
    help = "Create Halls for each existing cinema"

    def handle(self, *args, **options):
        # load all cinemas and delete all halls
        cinemas = Cinema.objects.all()
        Hall.objects.all().delete()

        # directories to images
        images_dir = os.path.join(settings.BASE_DIR, "images", "halls")
        schemes_dir = os.path.join(images_dir, "schemes")
        upper_banners_dir = os.path.join(images_dir, "upper_banners")
        gallery_dir = os.path.join(images_dir, "gallery")

        # access lists of all images of each folder
        scheme_images = os.listdir(schemes_dir)
        upper_banner_images = os.listdir(upper_banners_dir)
        gallery_images = os.listdir(gallery_dir)

        hall_images = []

        for cinema in cinemas:
            for i in range(3):
                scheme_image = random.choice(scheme_images)
                upper_banner_image = random.choice(upper_banner_images)

                hall = Hall(
                    cinema=cinema,
                    name_uk=f"Зал {i + 1}",
                    name_en=f"Hall {i + 1}",
                    description_uk=(
                        "Цей зал пропонує комфортабельні місця, чудову акустику та новітнє проекційне обладнання, "
                        "що забезпечує незабутній кінодосвід для кожного відвідувача."
                    ),
                    description_en=(
                        "This hall offers comfortable seating, excellent acoustics, and state-of-the-art projection equipment, "
                        "ensuring an unforgettable movie experience for every visitor."
                    ),
                    scheme=UploadedFile(file=open(os.path.join(schemes_dir, scheme_image), "rb")),
                    upper_banner=UploadedFile(file=open(os.path.join(upper_banners_dir, upper_banner_image), "rb")),
                    seo_url="https://imdb.com",
                    seo_title=f"Hall {i + 1} at {cinema.name_en} - Ultimate Movie Experience",
                    seo_description=(
                        f"Discover Hall {i + 1} at {cinema.name_en}, offering premium seating, top-notch acoustics, and "
                        "advanced projection systems for the best movie experience."
                    ),
                    seo_keywords=f"Hall {i + 1}, {cinema.name_en}, cinema, movie, experience, comfortable seating, advanced technology"
                )
                hall.save()

                selected_gallery_images = random.sample(gallery_images, 4)

                for gallery_image in selected_gallery_images:
                    hall_images.append(HallImage(
                        hall=hall,
                        image=UploadedFile(file=open(os.path.join(gallery_dir, gallery_image), "rb"))
                    ))

        HallImage.objects.bulk_create(hall_images)

        self.stdout.write(self.style.SUCCESS("Halls were created successfully"))
