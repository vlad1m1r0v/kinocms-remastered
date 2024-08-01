from django.db.models import Sum, Prefetch, Count
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView

from apps.schedule.models import Ticket, Schedule
from apps.users.models import CustomUser
from core.utilities.guards import admin_only


# Create your views here.
@admin_only
class AdminDashboardView(TemplateView):
    template_name = 'adminlte/panel/dashboard.html'


def admin_dashboard_statistics_view(request: HttpRequest):
    daily_revenue = (Ticket.objects.values('session__time__date')
                     .annotate(total_revenue=Sum('session__price'))
                     .order_by("session__time__date"))

    daily_revenues = {
        item['session__time__date'].strftime('%Y-%m-%d'): item['total_revenue']
        for item in daily_revenue
    }

    tickets = Ticket.objects.prefetch_related(
        Prefetch('session', queryset=Schedule.objects.prefetch_related('hall'))
    )

    cinemas = (
        tickets.values('session__hall__cinema__name_en')
        .annotate(total_tickets=Count('id'))
        .order_by('total_tickets')
    )

    films = (
        tickets.values('session__film__name_en')
        .annotate(total_tickets=Count('id'))
        .order_by('total_tickets')
    )

    users_count = CustomUser.objects.count()
    cinemas_count = cinemas.count()
    tickets_count = tickets.count()
    sessions_count = Schedule.objects.filter(time__gte=timezone.now().date()).count()

    popular_cinemas_by_tickets_sold = {cinema['session__hall__cinema__name_en']: cinema['total_tickets'] for cinema in
                                       cinemas}

    popular_films_by_tickets_sold = {film['session__film__name_en']: film['total_tickets'] for film in
                                     films}

    data = {
        'daily_revenues': daily_revenues,
        'popular_cinemas': popular_cinemas_by_tickets_sold,
        'tickets_count': tickets_count,
        'users_count': users_count,
        'cinemas_count': cinemas_count,
        'sessions_count': sessions_count,
        'popular_films': popular_films_by_tickets_sold
    }

    return JsonResponse(data, safe=False)
