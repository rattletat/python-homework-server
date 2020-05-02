from django.core.mail import send_mail
from django.shortcuts import redirect, reverse, render
from django.contrib import auth, messages

# from django.conf import settings
from accounts.forms import LoginForm

# LOGIN_MAIL_SENDER = settings.EMAIL_HOST_USER
MAIL_DISPLAYED_SENDER = "noreply@xyz321.de"
UNEXPECTED_FAILURE = (
    "Ein unerwarteter Fehler beim Absenden der Email ist aufgetreten."
    "Bitte kontaktiere Michael Brauweiler bei Slack."
)


def send_login_email(request):
    next = request.POST.get("next", reverse("home"))

    if request.method == "GET":
        return redirect(next)

    login = LoginForm(request.POST)
    if not login.is_valid():
        return render(request, "home.html", {"login": login})

    # Send mail
    try:
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
        user = login.save()
    except Exception:
        messages.error(request, UNEXPECTED_FAILURE)

    return redirect(next)


def login(request):
    next = request.POST.get("next", reverse("home"))
    token = request.GET.get("token")
    if token:
        user = auth.authenticate(uid=token)
        if user:
            user.email_verified = True
            auth.login(request, user)
        else:
            messages.error(
                request, "Dieser Nutzer existiert nicht!"
            )

    return redirect(next)
