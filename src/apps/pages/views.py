from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.pages.forms import MainPageForm
from apps.pages.models import MainPage
from core.utilities.guards import admin_only


@admin_only
class AdminPagesView(TemplateView):
    template_name = 'adminlte/panel/pages/pages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_page'] = MainPage.load()
        return context


@admin_only
class AdminMainPageView(TemplateView):
    template_name = 'adminlte/panel/pages/main_page.html'

    def get(self, *args, **kwargs):
        main_page = MainPage.load()
        form = MainPageForm(instance=main_page)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        instance = MainPage.load()
        form = MainPageForm(request.POST, instance=instance)

        if form.is_valid():
            form.save(commit=True)

            messages.success(request, "Main page was updated successfully")
            return redirect('adminlte_pages')

        messages.error(request, "Some errors occurred while updating main page")
        return self.render_to_response(self.get_context_data(form=form))
