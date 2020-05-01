from django.urls import path
from exercises import views

app_name = 'exercises'
urlpatterns = [
    path("<int:number>/", views.view_exercise, name="view_exercise"),
]
