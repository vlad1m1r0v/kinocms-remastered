from ajax_datatable.views import AjaxDatatableView
from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView

from core.utilities.guards import admin_only
from .forms import HallForm, HallImageFormSet
from .models import Hall, HallImage
from apps.cinemas.models import Cinema
from ..schedule.models import Schedule


class AdminHallsDataTableView(AjaxDatatableView):
    model = Hall
    title = 'Halls'
    initial_order = [["id", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': 'ID', 'visible': True, },
        {'name': 'name_en', 'title': 'Name', 'visible': True, },
        {'name': 'created_at', 'title': 'Creation Date', 'visible': True, },
        {'name': 'update_or_delete',
         'title': 'Update Or Delete',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False, },
    ]

    def get_initial_queryset(self, request: HttpRequest = None):
        queryset = self.model.objects.all()
        cinema_id = int(request.REQUEST.get(key='cinema_id'))
        queryset = queryset.filter(cinema_id=cinema_id)
        return queryset

    def customize_row(self, row, obj):
        row['update_or_delete'] = f"""
        <div class="d-flex flex-nowrap">
          <a href='{reverse('adminlte_halls_update_hall', kwargs={"hall_id": obj.id})}' class="btn btn-primary text-nowrap mr-2">
            <i class="fa fa-pen" aria-hidden="true"></i>
            Update
          </a>
          <a
            class="btn btn-info btn-danger text-nowrap"
            href='{reverse('adminlte_halls_delete_hall', kwargs={"hall_id": obj.id})}'
            data-toggle="modal"
            data-target="#confirmationModal"
          >
            <i class="fa fa-trash" aria-hidden="true"></i>
            Delete
          </a>
        </div>
        """


@admin_only
class AdminCreateHallView(TemplateView):
    template_name = 'adminlte/panel/hall.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        form = HallForm()
        formset = HallImageFormSet()
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, *args, **kwargs):
        cinema_id: int = kwargs.get('cinema_id')
        cinema = Cinema.objects.get(pk=cinema_id)

        form = HallForm(request.POST, request.FILES)
        formset = HallImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            hall = form.save(commit=False)
            hall.cinema = cinema
            hall.save()

            cinema.save()

            formset.instance = hall
            formset.save()

            messages.success(request, "Hall was created successfully")
            return redirect('adminlte_cinemas_update_cinema', cinema_id=cinema_id)

        messages.error(request, "Some errors occurred while creating hall")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminUpdateHallView(TemplateView):
    template_name = 'adminlte/panel/hall.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        hall_id: int = kwargs.get('hall_id')
        hall = Hall.objects.get(pk=hall_id)
        form = HallForm(instance=hall)
        formset = HallImageFormSet(instance=hall)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, *args, **kwargs):
        hall_id: int = kwargs.get('hall_id')
        hall = Hall.objects.get(pk=hall_id)
        cinema_id = hall.cinema_id

        form = HallForm(request.POST, request.FILES, instance=hall)
        formset = HallImageFormSet(request.POST, request.FILES, instance=hall)

        if form.is_valid() and formset.is_valid():
            form.save(commit=True)
            formset.save(commit=True)

            messages.success(request, "Hall was updated successfully")
            return redirect('adminlte_cinemas_update_cinema', cinema_id=cinema_id)

        messages.error(request, "Some errors occurred while updating hall")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteHallBannerView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        hall_id: int = kwargs.get('hall_id')
        Hall.objects.get(pk=hall_id).upper_banner.delete()
        return JsonResponse({"status": 202})


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteHallSchemeView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        hall_id: int = kwargs.get('hall_id')
        Hall.objects.get(pk=hall_id).scheme.delete()
        return JsonResponse({"status": 202})


@admin_only
class AdminDeleteHallView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        hall_id: int = kwargs.get('hall_id')
        hall = Hall.objects.get(pk=hall_id)
        cinema_id = hall.cinema_id
        hall.delete()
        messages.success(request, "Hall was deleted successfully")
        return redirect("adminlte_cinemas_update_cinema", cinema_id=cinema_id)


class HallDetailView(DetailView):
    model = Hall
    template_name = 'site/hall.html'
    context_object_name = 'hall'

    def get_queryset(self):
        today = timezone.now().date()

        return Hall.objects.prefetch_related(
            Prefetch('sessions', queryset=Schedule.objects.filter(time__date=today).only('id')),
            Prefetch('images', queryset=HallImage.objects.only('id', 'image')),
        )
