from django.core.management.base import BaseCommand
from apps.pages.models import MainPage


class Command(BaseCommand):
    help = "Create Main page for website"

    def handle(self, *args, **options):
        # delete page if exists
        MainPage.load().delete()

        # create page and fill it with data
        main_page = MainPage.load()
        main_page.is_active = True
        main_page.first_phone = "+380505050505"
        main_page.second_phone = "+380959595959"
        main_page.seo_title = "KinoSvit: Your Ultimate Movie Destination in Ukraine"
        main_page.seo_url = "https://www.imdb.com/"
        main_page.seo_keywords = "KinoSvit, cinema Ukraine, movie theaters Ukraine, movie tickets Ukraine, best cinema Ukraine, Ukrainian cinemas, blockbuster movies, indie movies, cinema experience, movie night, comfortable seating, delicious snacks, promotions, online booking."
        main_page.seo_text_en = " Immerse yourself in the magic of cinema at KinoSvit, Ukraine's leading movie theater chain. Experience breathtaking visuals and immersive sound on our state-of-the-art screens. From blockbuster hits to indie gems, we have something for everyone. Enjoy comfortable seating, delicious snacks, and exclusive promotions. Discover the perfect movie night with KinoSvit. Book your tickets now and embark on a cinematic adventure!"
        main_page.seo_text_uk = "Зануртеся у чарівний світ кіно з КіноСвіт, провідною мережею кінотеатрів в Україні. Відчуйте неймовірні візуальні ефекти та захоплюючий звук на наших сучасних екранах. Від блокбастерів до незалежного кіно - у нас є фільми на будь-який смак. Насолоджуйтесь комфортними кріслами, смачними закусками та ексклюзивними акціями. Відкрийте для себе ідеальний вечір кіно з КіноСвіт. Забронюйте квитки зараз і вирушайте у кіномандрівку!"
        main_page.seo_description = "Experience the ultimate movie magic in Ukraine. Enjoy blockbuster hits, indie gems, and comfortable seating on our state-of-the-art screens. Discover exclusive offers and book your tickets now!"
        main_page.save()

        self.stdout.write(
            self.style.SUCCESS("Main page was created successfully")
        )
