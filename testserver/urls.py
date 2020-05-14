from django.urls import path, include, re_path
from exercises.views import home_page as exercise_home
from exercises import urls as exercise_urls
from accounts import urls as accounts_urls
from django.contrib import admin
from django.contrib.flatpages import views as flatpages_views


urlpatterns = [
    path("", exercise_home, name="home"),
    path("exercise/", include(exercise_urls)),
    path("accounts/", include(accounts_urls)),
    path("admin/", admin.site.urls),
    path("django-rq/", include("django_rq.urls")),
    re_path(r"^(?P<url>.*/)$", flatpages_views.flatpage, name="flatpage"),
]
