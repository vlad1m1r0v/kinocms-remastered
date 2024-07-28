from django.db.models.functions import TruncDate
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView

from apps.cinemas.models import Cinema
from apps.films.models import Film
from apps.halls.models import Hall
from apps.schedule.models import Schedule


class ScheduleView(TemplateView):
    template_name = "site/schedule.html"


def schedule_cinemas_view(request: HttpRequest, *args, **kwargs):
    cinemas = Cinema.objects.values("id", "name_en", "name_uk")
    return JsonResponse(data=list(cinemas), safe=False)


def schedule_dates_view(request: HttpRequest, *args, **kwargs):
    distinct_dates = Schedule.objects.annotate(date=TruncDate('time')).values_list('date', flat=True).distinct()
    dates_list = list(distinct_dates)
    return JsonResponse(dates_list, safe=False)


def schedule_films_view(request: HttpRequest, *args, **kwargs):
    films = Film.objects.values("id", "name_en", "name_uk")
    return JsonResponse(data=list(films), safe=False)


def schedule_halls_view(request):
    cinema_id = request.GET.get('cinema_id')

    if cinema_id:
        halls = Hall.objects.filter(cinema_id=cinema_id)
    else:
        halls = Hall.objects.all()

    halls_list = list(halls.values('id', 'name_en', 'name_uk', 'cinema_id'))
    return JsonResponse(halls_list, safe=False)
