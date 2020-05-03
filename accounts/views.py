from django.shortcuts import redirect, render
from django.contrib import auth, messages
from smtplib import SMTPResponseException

# from django.conf import settings
from accounts.forms import LoginForm
from exercises.models import Exercise
from accounts.utils import send_email

MAIL_FAILURE = (
    "Ein unerwarteter Fehler beim Absenden der Email ist aufgetreten. "
    "Bitte kontaktiere Michael Brauweiler bei Slack."
)
MAIL_SUCCESS = "Dein Login Link ist soeben in deinem Email Postfach angekommen."
NO_SUCH_USER = "Dieser Nutzer existiert nicht!"


def send_login_email(request):
    login = LoginForm(request.POST)
    if not login.is_valid():
        # Print all form errors
        for error in login.errors.values():
            messages.error(request, error[0])
        exercises = Exercise.objects.all()
        return render(request, "home.html", {"exercises": exercises, "login": login})

    try:
        # Don't save user if email is invalid
        user = login.save(commit=False)
        send_email(request, user.uid, user.email)
        login.save()
        messages.success(request, MAIL_SUCCESS)
    except SMTPResponseException:
        messages.error(request, MAIL_FAILURE)

    return redirect("home")


def login(request):
    token = request.GET.get("token")
    if token:
        user = auth.authenticate(request, uid=token)
        if user:
            user.email_verified = True
            user.save()
            auth.login(request, user)
        else:
            messages.error(request, NO_SUCH_USER)

    return redirect('home')
