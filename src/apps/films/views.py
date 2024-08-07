from datetime import date, timedelta

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView

from apps.films.forms import FilmForm, FilmImageFormSet
from apps.films.models import Film
from apps.schedule.models import Schedule
from core.utilities.guards import admin_only


@admin_only
class AdminFilmsView(TemplateView):
    template_name = "adminlte/panel/films/films.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()

        current_films = Film.objects.filter(
            Q(created_at__lte=today - timedelta(7)),
        )
        context['current_films'] = current_films

        upcoming_films = Film.objects.filter(
            Q(created_at__gt=today - timedelta(7))
        )
        context['upcoming_films'] = upcoming_films

        return context


@admin_only
class AdminCreateFilmView(TemplateView):
    template_name = "adminlte/panel/films/film.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        form = FilmForm()
        formset = FilmImageFormSet()
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        form = FilmForm(request.POST, request.FILES)
        formset = FilmImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            film = form.save(commit=True)
            images = formset.save(commit=False)

            for image in images:
                image.film = film
                image.save()

            messages.success(request, "Film was created successfully")
            return redirect('adminlte_films')

        messages.error(request, "Some errors occurred while updating film")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminUpdateFilmView(TemplateView):
    template_name = "adminlte/panel/films/film.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        film_id: int = kwargs.get('film_id')
        film = Film.objects.get(id=film_id)
        form = FilmForm(instance=film)
        formset = FilmImageFormSet(instance=film)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, film_id: int):
        film = Film.objects.get(id=film_id)
        form = FilmForm(request.POST, request.FILES, instance=film)
        formset = FilmImageFormSet(request.POST, request.FILES, instance=film)

        if form.is_valid() and formset.is_valid():
            form.save(commit=True)
            formset.save(commit=True)

            messages.success(request, "Film was updated successfully")
            return redirect('adminlte_films')

        messages.error(request, "Some errors occurred while updating film")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        return context


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteFilmImageView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        film_id: int = kwargs.get('film_id')
        Film.objects.get(pk=film_id).image.delete()
        return JsonResponse({"status": 202})


@admin_only
class AdminDeleteFilmView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        film_id: int = kwargs.get('film_id')
        Film.objects.get(pk=film_id).delete()
        messages.success(request, "Film was deleted successfully")
        return redirect('adminlte_films')


class BillboardView(TemplateView):
    template_name = "site/films/billboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        sessions = Schedule.objects.filter(time__date=today) \
            .select_related('film') \
            .values('id', 'film__id', 'film__name_en', 'film__name_uk', 'film__image')

        context['sessions'] = sessions
        return context


class SoonView(TemplateView):
    template_name = "site/films/soon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        sessions = (Schedule.objects.filter(time__date__gt=today)
                    .select_related('film')
                    .values('film__id', 'time__date', 'film__name_en', 'film__name_uk', 'film__image')
                    .order_by('time__date'))

        context['sessions'] = sessions
        return context


class FilmView(DetailView):
    template_name = "site/films/film.html"
    model = Film
    context_object_name = "film"

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images')


def film_search_view(request: HttpRequest, *args, **kwargs):
    search = request.GET.get('search')
    films = (Film.objects
             .filter(Q(name_en__icontains=search) | Q(name_uk__icontains=search))
             .values('id', 'name_en', 'name_uk'))
    return JsonResponse(list(films), safe=False)
