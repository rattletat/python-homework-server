from django.contrib import admin
from django.contrib.flatpages import views as flat_views
from django.urls import include, path

from accounts import urls as accounts_urls
from exercises import urls as exercise_urls
from exercises.views import home_page as exercise_home

urlpatterns = [
    path("", exercise_home, name="home"),
    path("exercise/", include(exercise_urls)),
    path("accounts/", include(accounts_urls)),
    path("admin/", admin.site.urls),
    path("django-rq/", include("django_rq.urls")),
    path("impressum/", flat_views.flatpage, {"url": "/impressum/"}, name="impressum",),
]
