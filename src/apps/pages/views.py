from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from apps.pages.forms import MainPageForm, PageForm, PageImageFormSet, ContactsForm, ContactFormSet
from apps.pages.models import MainPage, Page, Contacts, Contact
from core.utilities.guards import admin_only


@admin_only
class AdminPagesView(TemplateView):
    template_name = 'adminlte/panel/pages/pages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_page'] = MainPage.load()
        context['contacts'] = Contacts.load()
        context['pages'] = Page.objects.all()
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


@admin_only
class AdminCreatePageView(TemplateView):
    template_name = 'adminlte/panel/pages/page.html'

    def get(self, request, *args, **kwargs):
        form = PageForm()
        formset = PageImageFormSet()

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST, request.FILES)
        formset = PageImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            page = form.save(commit=True)
            images = formset.save(commit=False)

            for image in images:
                image.page = page
                image.save()

            messages.success(request, "Page was created successfully")
            return redirect('adminlte_pages')

        messages.error(request, "Some errors occurred while creating page")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminUpdatePageView(TemplateView):
    template_name = "adminlte/panel/pages/page.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        page_id: int = kwargs.get('page_id')
        page = Page.objects.get(pk=page_id)
        form = PageForm(instance=page)
        formset = PageImageFormSet(instance=page)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, *args, **kwargs):
        page_id: int = kwargs.get('page_id')
        page = Page.objects.get(pk=page_id)
        form = PageForm(request.POST, request.FILES, instance=page)
        formset = PageImageFormSet(request.POST, request.FILES, instance=page)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            messages.success(request, "Page was updated successfully")
            return redirect('adminlte_pages')

        messages.error(request, "Some errors occurred while updating page")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminDeletePageView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        page_id = kwargs.get('page_id')
        page = Page.objects.get(pk=page_id)

        if not page.can_be_deleted:
            messages.error(request, "Page can't be deleted")
            return redirect("adminlte_pages")

        page.delete()
        messages.success(request, "Page was deleted successfully")
        return redirect("adminlte_pages")


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeletePageImageView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        page_id: int = kwargs.get('page_id')
        Page.objects.get(pk=page_id).image.delete()
        return JsonResponse({"status": 202})


@admin_only
class AdminContactsView(TemplateView):
    template_name = 'adminlte/panel/pages/contacts.html'

    def get(self, *args, **kwargs):
        contacts = Contacts.load()
        form = ContactsForm(instance=contacts)
        formset = ContactFormSet(instance=contacts)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, *args, **kwargs):
        instance = Contacts.load()
        form = ContactsForm(request.POST, request.FILES, instance=instance)
        formset = ContactFormSet(request.POST, request.FILES, instance=instance)

        if form.is_valid() and formset.is_valid():
            form.save(commit=True)
            formset.save(commit=True)

            messages.success(request, "Contacts were updated successfully")
            return redirect('adminlte_pages')

        messages.error(request, "Some errors occurred while updating contacts")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteContactLogoView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        contact_id: int = kwargs.get('contact_id')
        Contact.objects.get(pk=contact_id).logo.delete()
        return JsonResponse({"status": 202})


class MainPageView(TemplateView):
    template_name = "site/main.html"
