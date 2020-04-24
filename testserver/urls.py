from django.urls import path
from exercises.views import home_page as exercise_home
from exercises.views import view_exercise as exercise_view_exercise
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", exercise_home),
    path("exercise/<int:exercise_number>/", exercise_view_exercise),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
