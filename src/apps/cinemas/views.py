from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView, DetailView

from apps.cinemas.models import Cinema, CinemaImage
from core.utilities.guards import admin_only
from .forms import CinemaForm, CinemaImageFormSet
from ..halls.models import Hall
from ..schedule.models import Schedule


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

    def post(self, request: HttpRequest, *args, **kwargs):
        form = CinemaForm(request.POST, request.FILES)
        formset = CinemaImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            form = form.save(commit=True)
            formset = formset.save(commit=False)

            if form.is_valid() and formset.is_valid():
                form.save(commit=True)
                formset.save(commit=True)

            messages.success(request, "Cinema was created successfully")
            return redirect('adminlte_cinemas')

        messages.error(request, "Some errors occurred while creating cinema")
        self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminUpdateCinemaView(TemplateView):
    template_name = "adminlte/panel/cinemas/cinema.html"

    def get_context_data(self, *args, **kwargs):
        cinema_id: int = kwargs.get('cinema_id')
        cinema = Cinema.objects.get(id=cinema_id)
        context = super().get_context_data(**kwargs)
        context['form'] = CinemaForm(instance=cinema)
        context['formset'] = CinemaImageFormSet(instance=cinema)
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        cinema_id: int = kwargs.get('cinema_id')
        cinema = Cinema.objects.get(id=cinema_id)
        form = CinemaForm(request.POST, request.FILES, instance=cinema)
        formset = CinemaImageFormSet(request.POST, request.FILES, instance=cinema)

        if form.is_valid() and formset.is_valid():
            form.save(commit=True)
            formset.save(commit=True)

            messages.success(request, "Cinema was updated successfully")
            return redirect('adminlte_cinemas')

        messages.error(request, "Some errors occurred while updating cinema")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteCinemaBannerView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        cinema_id: int = kwargs.get('cinema_id')
        Cinema.objects.get(pk=cinema_id).upper_banner.delete()
        return JsonResponse({"status": 202})


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteCinemaLogoView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        cinema_id: int = kwargs.get('cinema_id')
        Cinema.objects.get(pk=cinema_id).logo.delete()
        return JsonResponse({"status": 202})


@admin_only
class AdminDeleteCinemaView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        cinema_id: int = kwargs.get('cinema_id')
        Cinema.objects.get(pk=cinema_id).delete()
        messages.success(request, "Cinema was deleted successfully")
        return redirect('adminlte_cinemas')


class CinemaListView(ListView):
    model = Cinema
    template_name = 'site/cinemas/cinemas_list.html'
    paginate_by = 10


class CinemaDetailView(DetailView):
    model = Cinema
    template_name = 'site/cinemas/cinema_detail.html'
    context_object_name = 'cinema'

    def get_queryset(self):
        today = timezone.now().date()

        return Cinema.objects.prefetch_related(
            Prefetch(
                'halls',
                queryset=Hall.objects.prefetch_related(
                    Prefetch('sessions', queryset=Schedule.objects.filter(time__date=today).only('id'))
                ).only('id', 'name_en', 'name_uk')
            ),
            Prefetch('images', queryset=CinemaImage.objects.only('id', 'image')),
        )
