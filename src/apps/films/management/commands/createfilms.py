from typing import TypedDict
from django.conf import settings
from os import listdir
from os.path import join
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand
from apps.films.models import Film, FilmImage


class FilmDict(TypedDict):
    name_en: str
    name_uk: str
    description_en: str
    description_uk: str
    images_url: str
    trailer_url: str
    is_3d: bool
    is_2d: bool
    is_imax: bool
    seo_url: str
    seo_title: str
    seo_description: str
    seo_keywords: str


images_dir = join(settings.BASE_DIR, "images", "films")

films_dicts: list[FilmDict] = [
    FilmDict(
        name_en="Spider-Man",
        name_uk="Людина-Павук",
        description_en="Peter Parker, an ordinary high school student, is bitten by a genetically altered spider and develops extraordinary abilities. Struggling to balance his newfound powers with his personal life, Peter must confront the villainous Green Goblin who threatens to destroy the city.",
        description_uk="Пітер Паркер, звичайний учень старшої школи, випадково отримує надзвичайні здібності після укусу генетично модифікованого павука. Боротьба з внутрішнім світом та новим статусом супергероя ускладнюється появою злочинця Зеленого Гобліна, який загрожує знищити місто.",
        images_url=join(images_dir, "spiderman"),
        trailer_url="https://www.youtube.com/watch?v=cqGjhVJWtEg",
        is_3d=True,
        is_2d=True,
        is_imax=True,
        seo_url="https://imdb.com",
        seo_title="Spider-Man - The Amazing Superhero",
        seo_description="Follow the thrilling journey of Peter Parker as he discovers his incredible spider-like abilities and becomes the iconic superhero, Spider-Man.",
        seo_keywords="Spider-Man, Peter Parker, superhero, comics, Marvel, Green Goblin, New York City, web-slinger"
    ),
    FilmDict(
        name_en="Project X",
        name_uk="Проект Ікс",
        description_en="Three high school underdogs decide to throw an epic party to boost their social status. What starts as a small gathering quickly spirals out of control, attracting thousands of uninvited guests and leading to a night of wild chaos, destruction, and unexpected consequences.",
        description_uk="Троє звичайних школярів вирішують влаштувати неймовірну вечірку, щоб стати популярними. Те, що мало бути невеликим зібранням друзів, перетворюється на шалене дійство з тисячами не запрошених гостей, руйнуванням та непередбачуваними наслідками.",
        images_url=join(images_dir, "projectx"),
        trailer_url="https://www.youtube.com/watch?v=HmrhuboNMtg",
        is_3d=True,
        is_2d=True,
        is_imax=False,
        seo_url="https://imdb.com",
        seo_title="Project X - The Ultimate Party",
        seo_description="Experience the craziest party ever thrown as three ordinary high school kids attempt to become the talk of the town, leading to a night of unforgettable mayhem.",
        seo_keywords="Project X, party, teenagers, comedy, teen movie, party movie, alcohol, drugs, police"
    ),
    FilmDict(
        name_en="Source Code",
        name_uk="Вихідний код",
        description_en="Captain Colter Stevens awakens to discover himself trapped in the body of a stranger aboard a rapidly approaching train disaster. With mere minutes until catastrophe strikes, he must repeatedly experience the same fateful journey, piecing together the puzzle to identify the bomber and avert tragedy.",
        description_uk="Капітан Кольтер Стівенс прокидається в тілі незнайомця в потязі, якому загрожує вибух. Маючи лише вісім хвилин, він змушений переживати один і той самий день знову і знову, намагаючись розгадати загадку бомбардувальника та запобігти катастрофі.",
        images_url=join(images_dir, "sourcecode"),
        trailer_url="https://www.youtube.com/watch?v=1HCsSOuDS7Y",
        is_3d=True,
        is_2d=False,
        is_imax=True,
        seo_url="https://imdb.com",
        seo_title="Source Code - A British Time Loop Thriller",
        seo_description="Experience the edge-of-your-seat tension as a British soldier is thrust into a time-loop to stop a deadly train explosion, facing a race against time to identify the bomber.",
        seo_keywords="Source Code, thriller, science fiction, time loop, explosion, déjà vu, bomb, terrorism"
    ),
    FilmDict(
        name_en="Who Am I",
        name_uk="Хто Я",
        description_en="Benjamin, a brilliant but socially awkward young hacker, is drawn into the world of cybercrime. As he becomes increasingly involved in a dangerous online game, he must confront his own identity and the consequences of his actions.",
        description_uk="Бенджамін, талановитий, але сором’язливий молодий хакер, потрапляє у світ кіберзлочинності. Захоплений небезпечною онлайн-грою, він стикається з питанням власної ідентичності та наслідками своїх дій.",
        images_url=join(images_dir, "whoami"),
        trailer_url="https://www.youtube.com/watch?v=lvM1o_mAT90",
        is_3d=False,
        is_2d=True,
        is_imax=True,
        seo_url="https://imdb.com",
        seo_title="Who Am I - A British Hacker Thriller",
        seo_description="Discover the intense world of cybercrime as a young British hacker faces the consequences of his online exploits and searches for his true identity.",
        seo_keywords="Who Am I, hacker, cybercrime, computer crime, identity, youth, drama, thriller"
    ),

]


class Command(BaseCommand):
    help = "Create Films for website"

    def handle(self, *args, **options):
        # delete all films first
        Film.objects.all().delete()

        # populate table with films
        films: list[Film] = []
        film_images: list[FilmImage] = []

        for films_dict in films_dicts:
            film = Film(
                name_en=films_dict["name_en"],
                name_uk=films_dict["name_uk"],
                description_en=films_dict["description_en"],
                description_uk=films_dict["description_uk"],
                trailer_url=films_dict["trailer_url"],
                image=UploadedFile(file=open(join(films_dict["images_url"], "image.jpg"), "rb")),
                is_imax=films_dict["is_imax"],
                is_2d=films_dict["is_2d"],
                is_3d=films_dict["is_3d"],
                seo_url=films_dict["seo_url"],
                seo_title=films_dict["seo_title"],
                seo_description=films_dict["seo_description"],
                seo_keywords=films_dict["seo_keywords"]
            )
            films.append(film)

            gallery_url = join(films_dict["images_url"], "gallery")

            film_images += [FilmImage(
                film=film,
                image=UploadedFile(file=open(join(gallery_url, image), "rb")),
            ) for image in listdir(gallery_url)]

        Film.objects.bulk_create(objs=films)
        FilmImage.objects.bulk_create(objs=film_images)

        self.stdout.write(
            self.style.SUCCESS("Films were created successfully")
        )
