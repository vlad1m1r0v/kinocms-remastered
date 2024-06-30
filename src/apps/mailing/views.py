from ajax_datatable.views import AjaxDatatableView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from .forms import SendingOptionForm, UploadTemplateForm
from .models import Template
from ..users.models import CustomUser


class AdminMailingView(TemplateView):
    template_name = 'adminlte/panel/mailing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sending_option'] = SendingOptionForm()
        context['upload_template'] = UploadTemplateForm()
        context['templates'] = Template.objects.all()[:5]
        return context


class AdminUploadTemplateView(View):
    @staticmethod
    def post(request):
        form = UploadTemplateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Template was uploaded successfully")
            return redirect("adminlte_mailing")

        messages.error(request, "Some errors occurred while uploading template")
        return redirect("adminlte_mailing")


class AdminDeleteTemplateView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        try:
            template_id = kwargs.get('template_id')
            Template.objects.filter(pk=template_id).delete()
            messages.success(request, "Template was deleted successfully")
        except ObjectDoesNotExist:
            messages.error(request, "Template does not exist")
        return redirect("adminlte_mailing")


class AdminMailingDatatableView(AjaxDatatableView):
    model = CustomUser
    title = 'Users'
    initial_order = [["id", "asc"], ]
    length_menu = [[1], [1]]
    search_values_separator = '+'

    column_defs = [
        {'name': 'select', 'title': 'Select', 'placeholder': True, 'searchable': False, 'orderable': False, },
        {'name': 'id', 'title': 'ID', 'visible': True, },
        {'name': 'created_at', 'title': 'Registration Date', 'visible': True, },
        {'name': 'birth_date', 'title': 'Birth Date', 'visible': True, },
        {'name': 'email', 'title': 'E-Mail', 'visible': True, },
        {'name': 'phone', 'title': 'Phone Number', 'visible': True, },
        {'name': 'full_name', 'title': 'Full name', 'visible': True, },
        {'name': 'nick_name', 'title': 'Nick Name', 'visible': True, },
        {'name': 'city', 'title': 'City', 'visible': True, },
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        )

    def customize_row(self, row, obj):
        row['select'] = "<input type=\"checkbox\" id={}>".format(obj.id)
