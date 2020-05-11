from django.urls import path, include
from exercises.views import home_page as exercise_home
from exercises import urls as exercise_urls
from accounts import urls as accounts_urls
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", exercise_home, name="home"),
    path("exercise/", include(exercise_urls)),
    path("accounts/", include(accounts_urls)),
    path("admin/", admin.site.urls),
    path('django-rq/', include('django_rq.urls'))
]
