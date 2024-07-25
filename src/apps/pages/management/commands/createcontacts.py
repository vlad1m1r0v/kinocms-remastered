from typing import TypedDict
from django.conf import settings
from os.path import join
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.pages.models import Contacts, Contact


class ContactDict(TypedDict):
    name_en: str
    name_uk: str
    address_en: str
    address_uk: str
    image_url: str
    lon: float
    lat: float


images_dir = join(settings.BASE_DIR, "images", "contacts")

contacts_dicts: list[ContactDict] = [
    ContactDict(
        name_en="IMax Chernihiv",
        name_uk="АйМакс в Чернігові",
        address_en="77 Guards Division Street, Building 1B, Chernihiv, Chernihiv Oblast, 14000, Ukraine",
        address_uk="вулиця 77-ї Гвардійської Дивізії, 1В, Чернігів, Чернігівська область, 14000",
        image_url=join(images_dir, "imax_chernihiv.jpg"),
        lon=51.5112754,
        lat=31.2987347,
    ),
    ContactDict(
        name_en="Ocean Plaza Kyiv",
        name_uk="Оушен Плаза в Києві",
        address_en="176, Antonovych Street, Kyiv, 03150, Ukraine",
        address_uk="вул. Антоновича, 176, Київ, 03150",
        image_url=join(images_dir, "ocean_plaza_kyiv.jpg"),
        lon=50.4124166,
        lat=30.5197306,
    ),
    ContactDict(
        name_en="Planet of Cinema",
        name_uk="Планета Кіно",
        address_en="Forum Lviv Shopping and Entertainment Center, 7B Pid Dubom Street, Lviv, Lviv Oblast, 79000, Ukraine",
        address_uk="ТРЦ «Forum Lviv», вулиця Під Дубом, 7Б, Львів, Львівська область, 79000",
        image_url=join(images_dir, "planeta_kino_lviv.jpg"),
        lon=50.4058355,
        lat=30.6087808,
    ),
]


class Command(BaseCommand):
    help = "Create Contacts for website"

    def handle(self, *args, **options):
        # clear contact page and all contacts information
        Contacts.load().delete()
        Contact.objects.all().delete()
        # create contact page and contacts for it
        contact_page = Contacts.load()
        contact_page.is_active = True
        contact_page.seo_title = "Contact KinoSvit - Get in Touch with Us"
        contact_page.seo_description = "Want to get in touch with KinoSvit? Find our contact information here. Discover our cinema locations, phone numbers, email addresses, and social media channels. Contact us for inquiries, feedback, or support. We are here to assist you!"
        contact_page.seo_keywords = "KinoSvit contacts, contact KinoSvit, cinema contacts Ukraine, Ukrainian cinema contact, contact us, cinema location, phone number, email address, social media, customer service, feedback, support"
        contact_page.seo_url = "https://www.imdb.com/"
        contact_page.save()

        contacts: list[Contact] = []
        for contact_dict in contacts_dicts:
            contacts.append(Contact(
                contacts=contact_page,
                name_en=contact_dict.get("name_en"),
                name_uk=contact_dict.get("name_uk"),
                address_en=contact_dict.get("address_en"),
                address_uk=contact_dict.get("address_uk"),
                logo=UploadedFile(file=open(contact_dict.get("image_url"), 'rb')),
                lon=contact_dict.get("lon"),
                lat=contact_dict.get("lat")
            ))

        Contact.objects.bulk_create(objs=contacts)

        self.stdout.write(
            self.style.SUCCESS("Contact page and contacts were created successfully")
        )
