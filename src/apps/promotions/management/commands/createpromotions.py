from typing import TypedDict
import os
from datetime import date
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.promotions.models import Promotions, PromotionsImage


class PromotionDict(TypedDict):
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


images_dir = os.path.join(settings.BASE_DIR, "images", "promotions")

promotions_dicts: list[PromotionDict] = [
    PromotionDict(
        name_en="For Students",
        name_uk="Для Студентів",
        description_en="Exclusive discounts and special offers for students. Enjoy your favorite movies at a fraction of the cost.",
        description_uk="Ексклюзивні знижки та спеціальні пропозиції для студентів. Насолоджуйтесь улюбленими фільмами за частину вартості.",
        images_url=os.path.join(images_dir, "for_students"),
        video_url="https://www.youtube.com/watch?v=Ph9C6iHla3Q",
        seo_url="https://imdb.com",
        seo_title="Student Promotions - Special Discounts and Offers",
        seo_description="Take advantage of our special student promotions, offering exclusive discounts and offers on your favorite movies.",
        seo_keywords="promotion, student, discount, special offer, cinema, movie"
    ),
    PromotionDict(
        name_en="For Children",
        name_uk="Для Дітей",
        description_en="Special offers and events tailored for children. Make your movie experience unforgettable with fun activities and discounts.",
        description_uk="Спеціальні пропозиції та заходи для дітей. Зробіть свій кінодосвід незабутнім з веселими заходами та знижками.",
        images_url=os.path.join(images_dir, "for_children"),
        video_url="https://www.youtube.com/watch?v=Ph9C6iHla3Q",
        seo_url="https://imdb.com",
        seo_title="Children's Promotions - Fun and Discounts",
        seo_description="Discover our promotions for children, including special offers and fun activities to enhance their movie experience.",
        seo_keywords="promotion, children, discount, fun, cinema, movie"
    ),
    PromotionDict(
        name_en="At Night",
        name_uk="Вночі",
        description_en="Experience the magic of cinema at night with our special late-night promotions. Enjoy exclusive discounts and a unique atmosphere.",
        description_uk="Відчуйте магію кіно вночі з нашими спеціальними нічними пропозиціями. Насолоджуйтесь ексклюзивними знижками та унікальною атмосферою.",
        images_url=os.path.join(images_dir, "at_night"),
        video_url="https://www.youtube.com/watch?v=Ph9C6iHla3Q",
        seo_url="https://imdb.com",
        seo_title="Night Promotions - Special Late-Night Offers",
        seo_description="Join us for late-night movie showings with exclusive discounts and a special atmosphere as part of our night promotions.",
        seo_keywords="promotion, night, discount, late-night, cinema, movie"
    ),
]


class Command(BaseCommand):
    help = "Create Promotions for website"

    def handle(self, *args, **options):
        # Delete all promotions first
        Promotions.objects.all().delete()

        # create promotions
        promotions = []
        promotions_images = []

        for promotion_dict in promotions_dicts:
            promotion = Promotions(
                is_active=True,
                publication_date=date.today(),
                name_uk=promotion_dict["name_uk"],
                name_en=promotion_dict["name_en"],
                description_uk=promotion_dict["description_uk"],
                description_en=promotion_dict["description_en"],
                image=UploadedFile(file=open(os.path.join(promotion_dict["images_url"], "image.jpg"), "rb")),
                video_url=promotion_dict["video_url"],
                seo_url=promotion_dict["seo_url"],
                seo_title=promotion_dict["seo_title"],
                seo_description=promotion_dict["seo_description"],
                seo_keywords=promotion_dict["seo_keywords"]
            )
            promotions.append(promotion)

            gallery_url = os.path.join(promotion_dict["images_url"], "gallery")
            gallery_images = os.listdir(gallery_url)

            for gallery_image in gallery_images:
                promotions_images.append(PromotionsImage(
                    promotion=promotion,
                    image=UploadedFile(file=open(os.path.join(gallery_url, gallery_image), "rb"))
                ))

        Promotions.objects.bulk_create(promotions)
        PromotionsImage.objects.bulk_create(promotions_images)

        self.stdout.write(self.style.SUCCESS("Promotions were created successfully"))
