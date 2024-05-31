from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import login, logout, authenticate

from .forms import LoginForm


class AdminLoginView(TemplateView):
    template_name = "adminlte/authentication/login.html"

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email: str = request.POST["email"]
            password: str = request.POST["password"]
            user = authenticate(email=email, password=password, is_superuser=True)
            if user:
                login(request, user)
                return redirect("adminlte_banners")
            else:
                messages.error(request, "Incorrect email or password")
        context = {"form": form}
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context


class AdminLogoutView(View):
    @staticmethod
    def post(request):
        logout(request)
        return redirect("adminlte_authentication_login")
