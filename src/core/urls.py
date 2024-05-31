from django.contrib import admin
from django.urls import path, include
from apps.users.views import AdminLoginView, AdminLogoutView
from apps.banners.views import BannersView

adminlte = [
    path("authentication/login/", AdminLoginView.as_view(), name="adminlte_authentication_login"),
    path("authentication/logout/", AdminLogoutView.as_view(), name="adminlte_authentication_logout"),
    path("banners/", BannersView.as_view(), name="adminlte_banners")
]

site = [

]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("adminlte/", include(adminlte)),
    path("/", include(site))
]
