from itertools import groupby
from operator import itemgetter, attrgetter

from django.db.models import Q, Prefetch, Subquery, OuterRef, Exists
from django.db.models.functions import TruncDate
from django.http import HttpRequest, JsonResponse
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView, DetailView
from django.template.defaultfilters import date as _date

from apps.cinemas.models import Cinema
from apps.films.models import Film
from apps.halls.models import Hall, Seat
from apps.schedule.models import Schedule, Ticket


class ScheduleView(TemplateView):
    template_name = "site/schedule/schedule_list.html"


def schedule_cinemas_view(request: HttpRequest, *args, **kwargs):
    cinemas = Cinema.objects.values("id", "name_en", "name_uk")
    return JsonResponse(data=list(cinemas), safe=False)


def schedule_dates_view(request: HttpRequest, *args, **kwargs):
    distinct_dates = (Schedule.objects
                      .annotate(date=TruncDate('time'))
                      .values_list('date', flat=True)
                      .distinct()
                      .order_by('date'))
    dates_list = list(distinct_dates)
    return JsonResponse(dates_list, safe=False)


def schedule_films_view(request: HttpRequest, *args, **kwargs):
    films = Film.objects.values("id", "name_en", "name_uk")
    return JsonResponse(data=list(films), safe=False)


def schedule_halls_view(request, *args, **kwargs):
    cinema_id = request.GET.get('cinema_id')

    if cinema_id:
        halls = Hall.objects.filter(cinema_id=cinema_id)
    else:
        halls = Hall.objects.all()

    halls_list = list(halls.values('id', 'name_en', 'name_uk', 'cinema_id'))
    return JsonResponse(halls_list, safe=False)


def schedule_sessions_view(request: HttpRequest, *args, **kwargs):
    is_3d = request.GET.get('is_3d')
    is_2d = request.GET.get('is_2d')
    is_imax = request.GET.get('is_imax')
    cinema_id = request.GET.get('cinema_id')
    date = request.GET.get('date')
    film_id = request.GET.get('film_id')
    hall_id = request.GET.get('hall_id')

    filters = Q()

    if is_3d is not None:
        filters &= Q(film__is_3d=True)
    if is_2d is not None:
        filters &= Q(film__is_2d=True)
    if is_imax is not None:
        filters &= Q(film__is_imax=True)
    if cinema_id:
        filters &= Q(hall__cinema_id=cinema_id)
    if date:
        date_obj = parse_date(date)
        if date_obj:
            filters &= Q(time__date=date_obj)
    if film_id:
        filters &= Q(film_id=film_id)
    if hall_id:
        filters &= Q(hall_id=hall_id)

    cinema_prefetch = Prefetch('hall__cinema')
    schedules = Schedule.objects.filter(filters).select_related('film', 'hall').prefetch_related(cinema_prefetch)

    schedules_list = [{
        'id': schedule.id,
        'date': _date(schedule.time, "d F, l"),
        'time': schedule.time.strftime("%H:%M"),
        'hall_id': schedule.hall.id,
        'hall_name_en': schedule.hall.name_en,
        'hall_name_uk': schedule.hall.name_uk,
        'film_id': schedule.film.id,
        'film_name_en': schedule.film.name_en,
        'film_name_uk': schedule.film.name_uk,
        'price': schedule.price
    } for schedule in schedules]

    grouped_by_date = groupby(schedules_list, itemgetter('date'))

    return JsonResponse({title: list(items) for title, items in grouped_by_date}, safe=False)


class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'site/schedule/schedule_detail.html'
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = self.object
        hall = schedule.hall
        film = schedule.film
        seats = hall.seats.all().order_by('row', 'column').annotate(
            is_free=Exists(Ticket.objects.filter(session=schedule, seat=OuterRef('pk')))
        )

        seats_by_row = {row: list(group) for row, group in groupby(seats, key=attrgetter('row'))}

        context['hall'] = hall
        context['film'] = film
        context['seats'] = seats_by_row
        return context
