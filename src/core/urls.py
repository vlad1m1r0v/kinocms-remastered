from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.films.views import AdminFilmsView, AdminCreateFilmView, AdminUpdateFilmView, AdminDeleteFilmImageView, \
    AdminDeleteFilmView
from apps.users.views import AdminLoginView, AdminLogoutView
from apps.banners.views import AdminBannersView, AdminBackgroundSettingsView, AdminTopBannersView, \
    AdminAdvertisementBannersView, AdminDeleteBackgroundView
from apps.cinemas.views import AdminCinemasView, AdminCreateCinemaView, AdminUpdateCinemaView, \
    AdminDeleteCinemaBannerView, AdminDeleteCinemaLogoView

adminlte = [
    path("authentication/login/", AdminLoginView.as_view(), name="adminlte_authentication_login"),
    path("authentication/logout/", AdminLogoutView.as_view(), name="adminlte_authentication_logout"),
    path("banners/", AdminBannersView.as_view(), name="adminlte_banners"),
    path("banners/background-settings/", AdminBackgroundSettingsView.as_view(),
         name="adminlte_banners_background_settings"),
    path("banners/background-settings/background/delete", AdminDeleteBackgroundView.as_view(),
         name="adminlte_banners_background_settings_banner_delete"),
    path("banners/top-banners/", AdminTopBannersView.as_view(), name="adminlte_banners_top_banners_settings"),
    path("banners/advertisement-banners/", AdminAdvertisementBannersView.as_view(),
         name="adminlte_banners_advertisement_banners_settings"),
    path("films/", AdminFilmsView.as_view(), name="adminlte_films"),
    path("films/create/", AdminCreateFilmView.as_view(), name="adminlte_films_create_film"),
    path("films/<int:film_id>/update/", AdminUpdateFilmView.as_view(), name="adminlte_films_update_film"),
    path("films/<int:film_id>/delete/", AdminDeleteFilmView.as_view(), name="adminlte_films_delete_film"),
    path("films/<int:film_id>/image", AdminDeleteFilmImageView.as_view(), name="adminlte_films_delete_film_image"),
    path("cinemas/", AdminCinemasView.as_view(), name="adminlte_cinemas"),
    path("cinemas/create/", AdminCreateCinemaView.as_view(), name="adminlte_cinemas_create_cinema"),
    path("cinemas/<int:cinema_id>/update/", AdminUpdateCinemaView.as_view(), name="adminlte_cinemas_update_cinema"),
    path("cinemas/<int:cinema_id>/banner/", AdminDeleteCinemaBannerView.as_view(),
         name="adminlte_cinema_delete_cinema_banner"),
    path("cinemas/<int:cinema_id>/logo/", AdminDeleteCinemaLogoView.as_view(),
         name="adminlte_cinema_delete_cinema_logo"),
]

site = [

]

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("adminlte/", include(adminlte)),
                  path("/", include(site))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
