from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.utils.translation import gettext as _, activate
from core.utilities.guards import admin_only
from .forms import LoginForm, RegisterForm, UserForm, ChangePasswordForm
from .models import CustomUser


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
                messages.success(request, "Logged in successfully")
                return redirect("adminlte_dashboard")
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


@admin_only
class AdminUsersView(TemplateView):
    template_name = "adminlte/panel/users/users.html"


class AdminUsersDatatableView(AjaxDatatableView):
    model = CustomUser
    title = 'Users'
    initial_order = [["id", "asc"], ]
    length_menu = [[10], [10]]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': 'ID', 'visible': True, },
        {'name': 'created_at', 'title': 'Registration Date', 'visible': True, },
        {'name': 'birth_date', 'title': 'Birth Date', 'visible': True, },
        {'name': 'email', 'title': 'E-Mail', 'visible': True, },
        {'name': 'phone', 'title': 'Phone Number', 'visible': True, },
        {'name': 'full_name', 'title': 'Full name', 'visible': True, },
        {'name': 'nick_name', 'title': 'Nick Name', 'visible': True, },
        {'name': 'city', 'title': 'City', 'visible': True, },
        {'name': 'update_or_delete',
         'title': 'Update Or Delete',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False, },
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        )

    def customize_row(self, row, obj):
        row['update_or_delete'] = f"""
        <div class="d-flex flex-nowrap">
          <a
          href='{reverse('adminlte_users_update_user', kwargs={'user_id': obj.id})}'
          class="btn btn-primary text-nowrap mr-2">
            <i class="fa fa-pen" aria-hidden="true"></i>
            Update
          </a>
          <a
            href='{reverse('adminlte_users_delete_user', kwargs={'user_id': obj.id})}'
            class="btn btn-info btn-danger text-nowrap"
            data-toggle="modal"
            data-target="#confirmationModal"
          >
            <i class="fa fa-trash" aria-hidden="true"></i>
            Delete
          </a>
        </div>
        """


@admin_only
class AdminUpdateUserView(TemplateView):
    template_name = 'adminlte/panel/users/user.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = CustomUser.objects.get(pk=user_id)
        form = UserForm(instance=user, prefix='form')
        reset_password = ChangePasswordForm(user=request.user, prefix='reset-password')
        return self.render_to_response(self.get_context_data(form=form, reset_password=reset_password))

    def post(self, request: HttpRequest, *args, **kwargs):
        user_id = kwargs.get('user_id')
        instance = CustomUser.objects.get(pk=user_id)
        form = UserForm(request.POST, instance=instance, prefix='form')
        reset_password = ChangePasswordForm(request.POST, prefix='reset-password', user=instance)

        if form.is_valid() and reset_password.is_valid():
            form.save()
            user = reset_password.save()

            messages.success(request, "User information was updated successfully")

            if user_id == request.user.id:
                update_session_auth_hash(request, user)

            return redirect('adminlte_users')

        messages.error(request, "Some errors occurred while updating user information")
        return self.render_to_response(self.get_context_data(form=form, reset_password=reset_password))


@admin_only
class AdminDeleteUserView(View):
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        user_id = kwargs.get('user_id')
        CustomUser.objects.filter(pk=user_id).delete()
        messages.success(request, "User was successfully deleted")

        if user_id == request.user.id:
            logout(request)
            return redirect('adminlte_authentication_login')

        return redirect("adminlte_users")


class RegisterView(TemplateView):
    template_name = "site/authentication/register.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=RegisterForm()))

    def post(self, request: HttpRequest, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("User registered successfully"))
            return redirect('site_authentication_login')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LoginView(TemplateView):
    template_name = "site/authentication/login.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=LoginForm()))

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email: str = request.POST["email"]
            password: str = request.POST["password"]
            user = authenticate(email=email, password=password, is_superuser=True)
            if user:
                login(request, user)
                messages.success(request, _("User logged in successfully"))
                return redirect("site_main")
            else:
                messages.error(request, _("Incorrect email or password"))
        context = {"form": form}
        return self.render_to_response(context=context)


class LogoutView(View):
    @staticmethod
    def post(request):
        logout(request)
        return redirect("site_authentication_login")


class ProfileView(TemplateView):
    template_name = 'site/profile.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        form = UserForm(instance=request.user, prefix='form')
        reset_password = ChangePasswordForm(user=request.user, prefix='reset-password')
        return self.render_to_response(self.get_context_data(form=form, reset_password=reset_password))

    def post(self, request: HttpRequest, *args, **kwargs):
        form = UserForm(request.POST, instance=request.user, prefix='form')
        reset_password = ChangePasswordForm(request.POST, prefix='reset-password', user=request.user)

        if form.is_valid() and reset_password.is_valid():
            form.save()
            user = reset_password.save()

            update_session_auth_hash(request, user)

            language: str = request.user.language
            activate(language)

            messages.success(request, _("User information was updated successfully"))

            return redirect(request.path_info)

        messages.error(request, _("Some errors occurred while updating user information"))
        return self.render_to_response(self.get_context_data(form=form, reset_password=reset_password))
