from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


def admin_only(cls):
    @method_decorator(user_passes_test(
        lambda u: u.is_staff and u.is_superuser,
        login_url=reverse_lazy("adminlte_authentication_login"),
        redirect_field_name=None
    ), name="dispatch")
    class AdminOnlyView(cls):
        pass

    return AdminOnlyView
