from django.db.models import Sum, Prefetch, Count
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView

from apps.schedule.models import Ticket, Schedule
from core.utilities.guards import admin_only


# Create your views here.
@admin_only
class AdminDashboardView(TemplateView):
    template_name = 'adminlte/panel/dashboard.html'


def admin_daily_revenue_view(request: HttpRequest, **kwargs):
    daily_revenue = Ticket.objects.values('session__time__date').annotate(total_revenue=Sum('session__price'))

    data = {
        item['session__time__date'].strftime('%Y-%m-%d'): item['total_revenue']
        for item in daily_revenue
    }

    return JsonResponse(data)


def admin_popular_cinemas_view(request):
    tickets = Ticket.objects.prefetch_related(
        Prefetch('session', queryset=Schedule.objects.prefetch_related('hall'))
    )

    cinemas = (
        tickets.values('session__hall__cinema__name_en')
        .annotate(total_tickets=Count('id'))
        .order_by('total_tickets')
    )

    data = {cinema['session__hall__cinema__name_en']: cinema['total_tickets'] for cinema in cinemas}

    return JsonResponse(data)
