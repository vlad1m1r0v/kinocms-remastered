from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.films.views import AdminFilmsView, AdminCreateFilmView, AdminUpdateFilmView, AdminDeleteFilmImageView, \
    AdminDeleteFilmView
from apps.users.views import AdminLoginView, AdminLogoutView, AdminUsersView, AdminUsersDatatableView, \
    AdminUpdateUserView, AdminDeleteUserView, LoginView, RegisterView, LogoutView, ProfileView
from apps.banners.views import AdminBannersView, AdminBackgroundSettingsView, AdminTopBannersView, \
    AdminAdvertisementBannersView, AdminDeleteBackgroundView
from apps.cinemas.views import AdminCinemasView, AdminCreateCinemaView, AdminUpdateCinemaView, \
    AdminDeleteCinemaBannerView, AdminDeleteCinemaLogoView, AdminDeleteCinemaView
from apps.halls.views import AdminHallsDataTableView, AdminCreateHallView, AdminUpdateHallView, \
    AdminDeleteHallSchemeView, AdminDeleteHallBannerView, AdminDeleteHallView
from apps.news.views import AdminNewsView, AdminCreateNewsView, AdminUpdateNewsView, AdminDeleteNewsImageView, \
    AdminNewsDataTableView, AdminDeleteNewsView, NewsListView, NewsDetailView
from apps.promotions.views import AdminPromotionsView, AdminPromotionsDataTableView, AdminCreatePromotionView, \
    AdminUpdatePromotionView, AdminDeletePromotionView, AdminDeletePromotionImageView
from apps.pages.views import AdminPagesView, AdminMainPageView, AdminCreatePageView, AdminUpdatePageView, \
    AdminDeletePageView, AdminDeletePageImageView, AdminContactsView, AdminDeleteContactLogoView, MainPageView, \
    ContactsPageView
from apps.mailing.views import AdminMailingView, AdminUploadTemplateView, AdminDeleteTemplateView, \
    AdminMailingDatatableView, admin_send_emails_view
from core.views import change_language_view

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
    path("cinemas/<int:cinema_id>/delete/", AdminDeleteCinemaView.as_view(), name="adminlte_cinemas_delete_cinema"),
    path("cinemas/<int:cinema_id>/banner/", AdminDeleteCinemaBannerView.as_view(),
         name="adminlte_cinema_delete_cinema_banner"),
    path("cinemas/<int:cinema_id>/logo/", AdminDeleteCinemaLogoView.as_view(),
         name="adminlte_cinema_delete_cinema_logo"),
    path("cinemas/<int:cinema_id>/halls/create/", AdminCreateHallView.as_view(), name="adminlte_halls_create_hall"),
    path("cinemas/<int:cinema_id>/halls/<int:hall_id>/update/", AdminUpdateHallView.as_view(),
         name="adminlte_halls_update_hall"),
    path("cinemas/<int:cinema_id>/halls/<int:hall_id>/delete/", AdminDeleteHallView.as_view(),
         name="adminlte_halls_delete_hall"),
    path("halls/datatable/", AdminHallsDataTableView.as_view(), name="adminlte_halls_datatable"),
    path("halls/<int:hall_id>/banner/", AdminDeleteHallBannerView.as_view(), name="adminlte_halls_delete_hall_banner"),
    path("halls/<int:hall_id>/scheme/", AdminDeleteHallSchemeView.as_view(), name="adminlte_halls_delete_hall_scheme"),
    path("news/", AdminNewsView.as_view(), name="adminlte_news"),
    path("news/datatable/", AdminNewsDataTableView.as_view(), name="adminlte_news_datatable"),
    path("news/create/", AdminCreateNewsView.as_view(), name="adminlte_news_create_news"),
    path("news/<int:news_id>/update/", AdminUpdateNewsView.as_view(), name="adminlte_news_update_news"),
    path("news/<int:news_id>/image/", AdminDeleteNewsImageView.as_view(),
         name="adminlte_news_delete_news_image"),
    path("news/<int:news_id>/delete/", AdminDeleteNewsView.as_view(),
         name="adminlte_news_delete_news"),
    path("promotions/", AdminPromotionsView.as_view(), name="adminlte_promotions"),
    path("promotions/datatable/", AdminPromotionsDataTableView.as_view(), name="adminlte_promotions_datatable"),
    path("promotions/create/", AdminCreatePromotionView.as_view(), name="adminlte_promotions_create_promotion"),
    path("promotions/<int:promotion_id>/update/", AdminUpdatePromotionView.as_view(),
         name="adminlte_promotions_update_promotion"),
    path("promotions/<int:promotion_id>/image/", AdminDeletePromotionImageView.as_view(),
         name="adminlte_promotions_delete_promotion_image"),
    path("promotions/<int:promotion_id>/delete/", AdminDeletePromotionView.as_view(),
         name="adminlte_promotions_delete_promotion"),
    path("pages/", AdminPagesView.as_view(), name="adminlte_pages"),
    path("pages/main/", AdminMainPageView.as_view(), name="adminlte_pages_main_page"),
    path("pages/create/", AdminCreatePageView.as_view(), name="adminlte_pages_create_page"),
    path("pages/<int:page_id>/update/", AdminUpdatePageView.as_view(), name="adminlte_pages_update_page"),
    path("pages/<int:page_id>/delete/", AdminDeletePageView.as_view(), name="adminlte_pages_delete_page"),
    path("pages/<int:page_id>/image/", AdminDeletePageImageView.as_view(), name="adminlte_pages_delete_page_image"),
    path("pages/contacts/", AdminContactsView.as_view(), name="adminlte_pages_contacts"),
    path("pages/contacts/<int:contact_id>/logo/", AdminDeleteContactLogoView.as_view(),
         name="adminlte_pages_contacts_delete_contact_logo"),
    path("users/", AdminUsersView.as_view(), name="adminlte_users"),
    path("users/datatable/", AdminUsersDatatableView.as_view(), name="adminlte_users_datatable"),
    path("users/<int:user_id>/update/", AdminUpdateUserView.as_view(), name="adminlte_users_update_user"),
    path("users/<int:user_id>/delete/", AdminDeleteUserView.as_view(), name="adminlte_users_delete_user"),
    path("mailing/", AdminMailingView.as_view(), name="adminlte_mailing"),
    path("mailing/upload/", AdminUploadTemplateView.as_view(), name="adminlte_mailing_upload_template"),
    path("mailing/templates/<int:template_id>/delete/", AdminDeleteTemplateView.as_view(),
         name="adminlte_mailing_delete_template"),
    path("mailing/datatable/", AdminMailingDatatableView.as_view(), name="adminlte_mailing_datatable"),
    path("mailing/send/", admin_send_emails_view, name="adminlte_mailing_send_email")
]

site = [
    path('change-language/', change_language_view, name='site_change_language'),
    path("authentication/register/", RegisterView.as_view(), name="site_authentication_register"),
    path("authentication/login/", LoginView.as_view(), name="site_authentication_login"),
    path("authentication/logout/", LogoutView.as_view(), name="site_authentication_logout"),
    path("main/", MainPageView.as_view(), name="site_main"),
    path("contacts/", ContactsPageView.as_view(), name="site_contacts"),
    path("profile/", ProfileView.as_view(), name="site_profile"),
    path("news/", NewsListView.as_view(), name="site_news"),
    path("news/<int:pk>", NewsDetailView.as_view(), name="site_news_detail")
]

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("adminlte/", include(adminlte)),
                  path("", include(site))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
