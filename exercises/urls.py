from django.urls import path

from . import views

app_name = "exercises"
urlpatterns = [
    path("<int:number>/", views.view_exercise, name="view_exercise"),
    path("<int:number>/results/", views.view_results, name="view_results"),
    path(
        "download/<int:resource_id>",
        views.download_public_file,
        name="download_public_file",
    ),
]
