from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView, DetailView

from apps.news.forms import NewsForm, NewsImageFormSet
from apps.news.models import News, NewsImage
from core.utilities.guards import admin_only


@admin_only
class AdminNewsView(TemplateView):
    template_name = 'adminlte/panel/news/news_table.html'


class AdminNewsDataTableView(AjaxDatatableView):
    model = News
    title = 'News'
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
        row['update_or_delete'] = f"""
        <div class="d-flex flex-nowrap">
          <a
          href='{reverse('adminlte_news_update_news', kwargs={'news_id': obj.id})}'
          class="btn btn-primary text-nowrap mr-2">
            <i class="fa fa-pen" aria-hidden="true"></i>
            Update
          </a>
          <a
            href='{reverse('adminlte_news_delete_news', kwargs={'news_id': obj.id})}'
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
class AdminCreateNewsView(TemplateView):
    template_name = 'adminlte/panel/news/news.html'

    def get(self, request, *args, **kwargs):
        form = NewsForm()
        formset = NewsImageFormSet()

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        form = NewsForm(request.POST, request.FILES)
        formset = NewsImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            news = form.save(commit=True)
            images = formset.save(commit=False)

            for image in images:
                image.news = news
                image.save()

            messages.success(request, "News were created successfully")
            return redirect('adminlte_news')

        print(form.errors)
        print(form.non_field_errors)

        messages.error(request, "Some errors occurred while creating news")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@admin_only
class AdminUpdateNewsView(TemplateView):
    template_name = "adminlte/panel/news/news.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        news_id: int = kwargs.get('news_id')
        news = News.objects.get(pk=news_id)
        form = NewsForm(instance=news)
        formset = NewsImageFormSet(instance=news)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request: HttpRequest, *args, **kwargs):
        news_id: int = kwargs.get('news_id')
        news = News.objects.get(pk=news_id)
        form = NewsForm(request.POST, request.FILES, instance=news)
        formset = NewsImageFormSet(request.POST, request.FILES, instance=news)

        if form.is_valid() and formset.is_valid():
            form.save(commit=True)
            formset.save(commit=True)

            messages.success(request, "News were updated successfully")
            return redirect('adminlte_news')

        messages.error(request, "Some errors occurred while updating news")
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteNewsImageView(View):
    @staticmethod
    def delete(request: HttpRequest, *args, **kwargs):
        news_id: int = kwargs.get('news_id')
        News.objects.get(pk=news_id).image.delete()
        return JsonResponse({"status": 202})


@admin_only
class AdminDeleteNewsView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        news_id: int = kwargs.get('news_id')
        News.objects.get(pk=news_id).delete()
        messages.success(request, "News were deleted successfully")
        return redirect("adminlte_news")


class NewsListView(ListView):
    template_name = 'site/news/news_list.html'
    paginate_by = 10
    queryset = News.objects.filter(is_active=True)


class NewsDetailView(DetailView):
    template_name = 'site/news/news_detail.html'
    model = News
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['images'] = NewsImage.objects.filter(news=self.object)
        return context
