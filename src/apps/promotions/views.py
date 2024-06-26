from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from apps.promotions.forms import PromotionsForm, PromotionsImageFormSet
from apps.promotions.models import Promotions
from core.utilities.guards import admin_only


@admin_only
class AdminPromotionsView(TemplateView):
    template_name = 'adminlte/panel/promotions/promotions_table.html'


class AdminPromotionsDataTableView(AjaxDatatableView):
    model = Promotions
    title = 'Promotions'
    initial_order = [["id", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': 'ID', 'visible': True, },
        {'name': 'name_en', 'title': 'Name', 'visible': True, },
        {'name': 'publication_date', 'title': 'Publication Date', 'visible': True, },
        {'name': 'is_active', 'title': 'Status', 'visible': True, },
        {'name': 'update_or_delete',
         'title': 'Update Or Delete',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False, },
    ]

    def customize_row(self, row, obj):
        row['update_or_delete'] = """
        <div class="d-flex flex-nowrap">
          <a class="btn btn-primary text-nowrap mr-2 update-promotion-button">
            <i class="fa fa-pen" aria-hidden="true"></i>
            Update
          </a>
          <a
            class="btn btn-info btn-danger text-nowrap"
            data-toggle="modal"
            data-target="#confirmationModal"
          >
            <i class="fa fa-trash" aria-hidden="true"></i>
            Delete
          </a>
        </div>
        """

        row['is_active'] = '<p>Enabled</p>' if obj.is_active else '<p>Disabled</p>'


@admin_only
class AdminCreatePromotionView(TemplateView):
    template_name = 'adminlte/panel/promotions/promotion.html'

    def get(self, request, *args, **kwargs):
        form = PromotionsForm()
        formset = PromotionsImageFormSet()

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        form = PromotionsForm(request.POST, request.FILES)
        formset = PromotionsImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            promotion = form.save(commit=True)
            images = formset.save(commit=False)

            for image in images:
                image.promotion = promotion
                image.save()

            messages.success(request, "Promotion was created successfully")
            return redirect('adminlte_promotions')

        messages.error(request, "Some errors occurred while creating promotion")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminUpdatePromotionView(TemplateView):
    template_name = "adminlte/panel/promotions/promotion.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        promotion_id: int = kwargs.get('promotion_id')
        promotion = Promotions.objects.get(pk=promotion_id)
        form = PromotionsForm(instance=promotion)
        formset = PromotionsImageFormSet(instance=promotion)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, *args, **kwargs):
        promotion_id: int = kwargs.get('promotion_id')
        promotion = Promotions.objects.get(pk=promotion_id)
        form = PromotionsForm(request.POST, request.FILES, instance=promotion)
        formset = PromotionsImageFormSet(request.POST, request.FILES, instance=promotion)

        if form.is_valid() and formset.is_valid():
            form.save(commit=True)
            formset.save(commit=True)

            messages.success(request, "Promotion was updated successfully")
            return redirect('adminlte_promotions')

        messages.error(request, "Some errors occurred while updating promotion")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeletePromotionImageView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        promotion_id: int = kwargs.get('promotion_id')
        Promotions.objects.get(pk=promotion_id).image.delete()
        return JsonResponse({"status": 202})


@admin_only
class AdminDeletePromotionView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        promotion_id: int = kwargs.get('promotion_id')
        Promotions.objects.get(pk=promotion_id).delete()
        messages.success(request, "Promotion was deleted successfully")
        return redirect("adminlte_promotions")
