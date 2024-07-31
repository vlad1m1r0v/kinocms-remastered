from django.db.models import Sum
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView

from apps.schedule.models import Ticket


# Create your views here.
class AdminDashboardView(TemplateView):
    template_name = 'adminlte/panel/dashboard.html'


def admin_daily_revenue_view(request: HttpRequest, **kwargs):
    daily_revenue = Ticket.objects.values('session__time__date').annotate(total_revenue=Sum('session__price'))

    data = {
        item['session__time__date'].strftime('%Y-%m-%d'): item['total_revenue']
        for item in daily_revenue
    }

    return JsonResponse(data)
