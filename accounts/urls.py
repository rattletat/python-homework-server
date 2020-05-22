from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import login, send_login_email

app_name = 'accounts'
urlpatterns = [
    path("send_login_email", send_login_email, name="send_login_email"),
    path("login", login, name="login"),
    path('logout', LogoutView.as_view(), name='logout'),
]
