from typing import TypedDict
import os
from datetime import date
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.news.models import News, NewsImage


class NewsDict(TypedDict):
    name_en: str
    name_uk: str
    description_en: str
    description_uk: str
    images_url: str
    video_url: str
    seo_url: str
    seo_title: str
    seo_description: str
    seo_keywords: str


images_dir = os.path.join(settings.BASE_DIR, "images", "news")

news_dicts: list[NewsDict] = [
    NewsDict(
        name_en="We Are Open",
        name_uk="Ми Відкриті",
        description_en="We are excited to announce that our cinema is now open. Join us to enjoy the latest movies in a safe and comfortable environment.",
        description_uk="Ми раді повідомити, що наш кінотеатр тепер відкритий. Приєднуйтесь до нас, щоб насолоджуватися найновішими фільмами у безпечному та комфортному середовищі.",
        images_url=os.path.join(images_dir, "we_are_open"),
        video_url="https://www.youtube.com/watch?v=TLZ3ZDICisM",
        seo_url="https://imdb.com",
        seo_title="We Are Open - Join Us for the Latest Movies",
        seo_description="Our cinema is now open! Enjoy the latest movies in a safe and comfortable environment.",
        seo_keywords="news, cinema, open, movies, safe, comfortable"
    ),
    NewsDict(
        name_en="We Have a Mobile App",
        name_uk="У Нас Є Мобільний Додаток",
        description_en="Download our new mobile app to book tickets, check showtimes, and get the latest updates on your favorite movies.",
        description_uk="Завантажте наш новий мобільний додаток, щоб бронювати квитки, перевіряти розклад та отримувати останні новини про улюблені фільми.",
        images_url=os.path.join(images_dir, "we_have_mobile_app"),
        video_url="https://www.youtube.com/watch?v=TLZ3ZDICisM",
        seo_url="https://imdb.com",
        seo_title="New Mobile App - Book Tickets and Check Showtimes",
        seo_description="Get our new mobile app to book tickets, check showtimes, and stay updated on your favorite movies.",
        seo_keywords="news, mobile app, book tickets, showtimes, movies, updates"
    ),
    NewsDict(
        name_en="Electricity Outage",
        name_uk="Відключення Електроенергії",
        description_en="Due to an electricity outage, our cinema will be closed temporarily. We apologize for any inconvenience and will keep you updated.",
        description_uk="Через відключення електроенергії наш кінотеатр буде тимчасово закритий. Просимо вибачення за незручності та будемо тримати вас у курсі подій.",
        images_url=os.path.join(images_dir, "electricity_outage"),
        video_url="https://www.youtube.com/watch?v=TLZ3ZDICisM",
        seo_url="https://imdb.com",
        seo_title="Electricity Outage - Cinema Temporarily Closed",
        seo_description="Our cinema is temporarily closed due to an electricity outage. We apologize for the inconvenience and will keep you updated.",
        seo_keywords="news, electricity outage, cinema closed, inconvenience, updates"
    ),
]


class Command(BaseCommand):
    help = "Create News for website"

    def handle(self, *args, **options):
        # Delete all news first
        News.objects.all().delete()

        news = []
        news_images = []

        # Fill news table with data
        for news_dict in news_dicts:
            news_item = News(
                is_active=True,
                publication_date=date.today(),
                name_uk=news_dict["name_uk"],
                name_en=news_dict["name_en"],
                description_uk=news_dict["description_uk"],
                description_en=news_dict["description_en"],
                image=UploadedFile(file=open(os.path.join(news_dict["images_url"], "image.jpg"), "rb")),
                video_url=news_dict["video_url"],
                seo_url=news_dict["seo_url"],
                seo_title=news_dict["seo_title"],
                seo_description=news_dict["seo_description"],
                seo_keywords=news_dict["seo_keywords"]
            )
            news.append(news_item)

            gallery_url = os.path.join(news_dict["images_url"], "gallery")
            gallery_images = os.listdir(gallery_url)

            for gallery_image in gallery_images:
                news_images.append(NewsImage(
                    news=news_item,
                    image=UploadedFile(file=open(os.path.join(gallery_url, gallery_image), "rb"))
                ))

        News.objects.bulk_create(news)
        NewsImage.objects.bulk_create(news_images)

        self.stdout.write(self.style.SUCCESS("News were created successfully"))
