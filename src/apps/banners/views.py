from django.views.generic import TemplateView


class BannersView(TemplateView):
    template_name = "adminlte/panel/banners.html"
