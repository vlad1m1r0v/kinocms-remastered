from typing import TypedDict
from django.conf import settings
from os import listdir
from os.path import join
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.pages.models import Page, PageImage


class PageDict(TypedDict):
    name_en: str
    name_uk: str
    description_en: str
    description_uk: str
    images_url: str
    seo_url: str
    seo_title: str
    seo_description: str
    seo_keywords: str


images_dir = join(settings.BASE_DIR, "images", "pages")

pages_dicts: list[PageDict] = [
    PageDict(
        name_en="Cafe-Bar",
        name_uk="Кафе-Бар",
        description_en="Enjoy a variety of snacks and drinks at our cafe-bar before or after your movie.",
        description_uk="Насолоджуйтесь різноманітними закусками та напоями в нашому кафе-барі перед або після фільму.",
        images_url=join(images_dir, "cafebar"),
        seo_url="https://imdb.com",
        seo_title="Cafe-Bar - Relax and Enjoy",
        seo_description="Relax and enjoy a variety of snacks and drinks at our cozy cafe-bar.",
        seo_keywords="Cafe-Bar, snacks, drinks, relaxation, cinema"
    ),
    PageDict(
        name_en="VIP Hall",
        name_uk="VIP Зал",
        description_en="Experience luxury and comfort in our VIP Hall with premium seating and exclusive services.",
        description_uk="Відчуйте розкіш та комфорт у нашому VIP Залі з преміум-сидіннями та ексклюзивними послугами.",
        images_url=join(images_dir, "viphall"),
        seo_url="https://imdb.com",
        seo_title="VIP Hall - Luxury and Comfort",
        seo_description="Enjoy the ultimate movie experience with premium seating and exclusive services in our VIP Hall.",
        seo_keywords="VIP Hall, luxury, comfort, premium seating, exclusive services"
    ),
    PageDict(
        name_en="Child Room",
        name_uk="Дитяча Кімната",
        description_en="A special area for children to play and enjoy while parents watch a movie.",
        description_uk="Особлива зона для дітей, де вони можуть гратися та насолоджуватися часом, поки батьки дивляться фільм.",
        images_url=join(images_dir, "childroom"),
        seo_url="https://imdb.com",
        seo_title="Child Room - Fun for Kids",
        seo_description="A safe and fun environment for children to play while their parents enjoy a movie.",
        seo_keywords="Child Room, kids, play area, family friendly, cinema"
    ),
    PageDict(
        name_en="For Advertisers",
        name_uk="Для Рекламодавців",
        description_en="Advertise your products and services on the big screen to a captive audience.",
        description_uk="Рекламуйте свої продукти та послуги на великому екрані перед захопленою аудиторією.",
        images_url=join(images_dir, "advertisers"),
        seo_url="https://imdb.com",
        seo_title="For Advertisers - Reach Your Audience",
        seo_description="Promote your brand on the big screen and reach a wide audience with our advertising opportunities.",
        seo_keywords="For Advertisers, advertising, marketing, cinema, big screen"
    ),
    PageDict(
        name_en="Mobile Applications",
        name_uk="Мобільні Додатки",
        description_en="Stay connected with our cinema through our mobile applications. Book tickets, check showtimes, and more.",
        description_uk="Будьте на зв'язку з нашим кінотеатром через наші мобільні додатки. Бронюйте квитки, перевіряйте розклад та багато іншого.",
        images_url=join(images_dir, "mobileapps"),
        seo_url="https://imdb.com",
        seo_title="Mobile Applications - Stay Connected",
        seo_description="Download our mobile applications to book tickets, check showtimes, and stay connected with our cinema.",
        seo_keywords="Mobile Applications, app, cinema, tickets, showtimes"
    ),
    PageDict(
        name_en="About Cinema",
        name_uk="Про Кінотеатр",
        description_en="Learn more about our cinema chain, our history, and our commitment to providing the best movie experience.",
        description_uk="Дізнайтеся більше про нашу мережу кінотеатрів, нашу історію та наше прагнення надавати найкращий кінодосвід.",
        images_url=join(images_dir, "aboutcinema"),
        seo_url="https://imdb.com",
        seo_title="About Cinema - Our Story",
        seo_description="Discover the story of our cinema chain and our dedication to providing an exceptional movie experience.",
        seo_keywords="About Cinema, cinema chain, history, movie experience"
    ),
]


class Command(BaseCommand):
    help = "Create Pages for website"

    def handle(self, *args, **options):
        # delete all pages first
        Page.objects.all().delete()

        # populate table with pages
        pages: list[Page] = []
        page_images: list[PageImage] = []

        for page_dict in pages_dicts:
            page = Page(
                name_en=page_dict["name_en"],
                name_uk=page_dict["name_uk"],
                description_en=page_dict["description_en"],
                description_uk=page_dict["description_uk"],
                image=UploadedFile(file=open(join(page_dict["images_url"], "image.jpg"), "rb")),
                seo_url=page_dict["seo_url"],
                seo_title=page_dict["seo_title"],
                seo_description=page_dict["seo_description"],
                seo_keywords=page_dict["seo_keywords"]
            )
            pages.append(page)

            gallery_url = join(page_dict["images_url"], "gallery")

            page_images += [PageImage(
                page=page,
                image=UploadedFile(file=open(join(gallery_url, image), "rb")),
            ) for image in listdir(gallery_url)]

        Page.objects.bulk_create(objs=pages)
        PageImage.objects.bulk_create(objs=page_images)

        self.stdout.write(self.style.SUCCESS("Pages were created successfully"))
