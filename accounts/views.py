from django.core.mail import send_mail
from django.shortcuts import redirect, reverse, render
from django.contrib import auth, messages
from smtplib import SMTPResponseException

# from django.conf import settings
from accounts.forms import LoginForm
from exercises.models import Exercise

# LOGIN_MAIL_SENDER = settings.EMAIL_HOST_USER
MAIL_DISPLAYED_SENDER = "noreply@xyz321.de"
SEND_MAIL_FAILURE = (
    "Ein unerwarteter Fehler beim Absenden der Email ist aufgetreten. "
    "Bitte kontaktiere Michael Brauweiler bei Slack."
)


def send_login_email(request):
    login = LoginForm(request.POST)
    if not login.is_valid():
        for error in login.errors.values():
            messages.error(request, error[0])
        exercises = Exercise.objects.all()
        return render(request, "home.html", {"exercises": exercises, "login": login})

    try:
        # If email is invalid don't save user
        user = login.save(commit=False)
        url = request.build_absolute_uri(
            reverse("accounts:login") + "?token=" + str(user.uid)
        )
        message_body = (
            f"Benutze diesen Link um dich auf der Seite einzuloggen:\n\n{url}"
        )
        send_mail(
            "Dein Login Link für 'Programmieren für Sozialwissenschaftler*innen'",
            message_body,
            MAIL_DISPLAYED_SENDER,
            [user.email],
        )
        messages.success(
            request, "Dein Login Link ist soeben in deinem Email Postfach angekommen."
        )
        login.save()
    except SMTPResponseException:
        messages.error(request, SEND_MAIL_FAILURE)
    return redirect("home")


def login(request):
    token = request.GET.get("token")
    if token:
        user = auth.authenticate(uid=token)
        if user:
            user.email_verified = True
            user.save()
            auth.login(request, user)
        else:
            messages.error(request, "Dieser Nutzer existiert nicht!")

    return redirect('home')