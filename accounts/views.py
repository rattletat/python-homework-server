from django.core.mail import send_mail
from django.shortcuts import redirect, reverse
from django.contrib import auth, messages
from accounts.models import Token
from django.conf import settings

LOGIN_MAIL_SENDER = settings.EMAIL_HOST_USER


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse("accounts:login") + "?token=" + str(token.uid)
    )
    message_body = f"Benutze diesen Link um dich auf der Seite einzuloggen:\n\n{url}"
    send_mail(
        "Dein Login Link für 'Programmieren für Sozialwissenschaftler*innen'",
        message_body,
        LOGIN_MAIL_SENDER,
        [email],
    )
    messages.success(
        request, "Dein Login Link ist soeben in deinem Email Postfach angekommen."
    )
    return redirect("home")


def login(request):
    token = request.GET.get('token')
    user = auth.authenticate(uid=token)
    if user:
        auth.login(request, user)
    return redirect("home")
