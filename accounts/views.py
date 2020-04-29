from django.shortcuts import render, redirect
import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.mail import send_mail

from accounts.models import Token


def send_login_email(request):
    email = request.POST["email"]
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print("saving uid", uid, "for email", email, file=sys.stderr)
    url = request.build_absolute_uri(f"/accounts/login?uid={uid}")
    send_mail(
        "Dein Login Link für 'Programmieren für Sozialwissenschaftler*innen'",
        f"""Benutze diesen Link um dich auf der Seite einzuloggen und deine Hausaufgaben abzugeben:
        \n\n{url}
        \n\n Halte diese URL geheim!""",
        "noreply@xyz321.de",
        [email],
    )
    return render(request, "login_email_sent.html")


def login(request):
    print("login view", file=sys.stderr)
    uid = request.GET.get("uid")
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect("/")


def logout(request):
    auth_logout(request)
    return redirect("/")
