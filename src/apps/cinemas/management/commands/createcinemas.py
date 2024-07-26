from typing import TypedDict
from django.conf import settings
from os import listdir
from os.path import join
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.cinemas.models import Cinema, CinemaImage


class CinemaDict(TypedDict):
    name_en: str
    name_uk: str
    description_en: str
    description_uk: str
    features_en: str
    features_uk: str
    logo_url: str
    upper_banner_url: str
    images_url: str
    seo_url: str
    seo_title: str
    seo_description: str
    seo_keywords: str


images_dir = join(settings.BASE_DIR, "images", "cinemas")

cinemas_dicts: list[CinemaDict] = [
    CinemaDict(
        name_en="IMax Chernihiv",
        name_uk="IMax Чернігів",
        description_en="Experience the ultimate movie watching at IMax Chernihiv with stunning visuals and sound.",
        description_uk="Насолоджуйтесь найкращими враженнями від перегляду фільмів у IMax Чернігів з вражаючими візуальними та звуковими ефектами.",
        features_en="3D, 4K projection, Dolby Atmos",
        features_uk="3D, 4K проекція, Dolby Atmos",
        logo_url=join(images_dir, "imax_chernihiv", "image.jpg"),
        upper_banner_url=join(images_dir, "imax_chernihiv", "upper_banner.jpg"),
        images_url=join(images_dir, "imax_chernihiv", "gallery"),
        seo_url="https://imdb.com",
        seo_title="IMax Chernihiv - Ultimate Movie Experience",
        seo_description="Enjoy the best movie experience at IMax Chernihiv with stunning visuals and sound.",
        seo_keywords="IMax, Chernihiv, cinema, movie experience, 3D, 4K, Dolby Atmos"
    ),
    CinemaDict(
        name_en="Ocean Plaza Kyiv",
        name_uk="Ocean Plaza Київ",
        description_en="Ocean Plaza Kyiv offers a luxurious movie experience with comfortable seating and premium services.",
        description_uk="Ocean Plaza Київ пропонує розкішний кінодосвід з комфортними сидіннями та преміум послугами.",
        features_en="Recliner seats, VIP lounges, gourmet snacks",
        features_uk="Реклайнери, VIP лаунжі, вишукані закуски",
        logo_url=join(images_dir, "ocean_plaza_kyiv", "image.jpg"),
        upper_banner_url=join(images_dir, "ocean_plaza_kyiv", "upper_banner.jpg"),
        images_url=join(images_dir, "ocean_plaza_kyiv", "gallery"),
        seo_url="https://imdb.com",
        seo_title="Ocean Plaza Kyiv - Luxurious Movie Experience",
        seo_description="Experience luxury at Ocean Plaza Kyiv with comfortable seating and premium services.",
        seo_keywords="Ocean Plaza, Kyiv, cinema, luxury, recliner seats, VIP, gourmet snacks"
    ),
    CinemaDict(
        name_en="Planeta Kino Lviv",
        name_uk="Планета Кіно Львів",
        description_en="Planeta Kino Lviv is known for its advanced technology and exceptional movie experience.",
        description_uk="Планета Кіно Львів відома своєю передовою технологією та винятковим кінодосвідом.",
        features_en="IMAX, 4DX, ScreenX",
        features_uk="IMAX, 4DX, ScreenX",
        logo_url=join(images_dir, "planeta_kino_lviv", "image.jpg"),
        upper_banner_url=join(images_dir, "planeta_kino_lviv", "upper_banner.jpg"),
        images_url=join(images_dir, "planeta_kino_lviv", "gallery"),
        seo_url="https://imdb.com",
        seo_title="Planeta Kino Lviv - Advanced Movie Technology",
        seo_description="Discover advanced movie technology at Planeta Kino Lviv for an exceptional movie experience.",
        seo_keywords="Planeta Kino, Lviv, cinema, IMAX, 4DX, ScreenX, advanced technology"
    ),
]


class Command(BaseCommand):
    help = "Create Cinemas for website"

    def handle(self, *args, **options):
        # delete all cinemas first
        Cinema.objects.all().delete()

        # populate table with cinemas
        cinemas: list[Cinema] = []
        cinema_images: list[CinemaImage] = []

        for cinema_dict in cinemas_dicts:
            cinema = Cinema(
                name_en=cinema_dict["name_en"],
                name_uk=cinema_dict["name_uk"],
                description_en=cinema_dict["description_en"],
                description_uk=cinema_dict["description_uk"],
                features_en=cinema_dict["features_en"],
                features_uk=cinema_dict["features_uk"],
                logo=UploadedFile(file=open(cinema_dict["logo_url"], "rb")),
                upper_banner=UploadedFile(file=open(cinema_dict["upper_banner_url"], "rb")),
                seo_url=cinema_dict["seo_url"],
                seo_title=cinema_dict["seo_title"],
                seo_description=cinema_dict["seo_description"],
                seo_keywords=cinema_dict["seo_keywords"]
            )
            cinemas.append(cinema)

            gallery_url = cinema_dict["images_url"]

            cinema_images += [CinemaImage(
                cinema=cinema,
                image=UploadedFile(file=open(join(gallery_url, image), "rb")),
            ) for image in listdir(gallery_url)]

        Cinema.objects.bulk_create(objs=cinemas)
        CinemaImage.objects.bulk_create(objs=cinema_images)

        self.stdout.write(self.style.SUCCESS("Cinemas were created successfully"))
