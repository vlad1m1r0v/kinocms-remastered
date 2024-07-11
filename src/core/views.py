from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "site/main.html"
