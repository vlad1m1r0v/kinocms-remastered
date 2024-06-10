from django.views.generic import TemplateView

from apps.cinemas.models import Cinema
from core.utilities.guards import admin_only
from .forms import CinemaForm, CinemaImageFormSet


@admin_only
class AdminCinemasView(TemplateView):
    template_name = "adminlte/panel/cinemas/cinemas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cinemas'] = Cinema.objects.all()
        return context


@admin_only
class AdminCreateCinemaView(TemplateView):
    template_name = "adminlte/panel/cinemas/cinema.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CinemaForm()
        context['formset'] = CinemaImageFormSet()
        return context
