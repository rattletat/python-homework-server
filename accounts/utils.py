from django.core import mail
from django.shortcuts import reverse


def send_email(request, token, target_email):
    url = request.build_absolute_uri(reverse("accounts:login") + "?token=" + str(token))
    displayed_sender = "noreply@xyz321.de"
    subject = "Dein Login Link für 'Programmieren für Sozialwissenschaftler*innen'"
    message_body = (
        "Benutze diesen Link um dich auf der Seite einzuloggen:\n"
        "\n"
        f"{url}\n"
        "\n"
        "Halte diese URL unter allen Umständen geheim!"
    )
    mail.send_mail(subject, message_body, displayed_sender, [target_email])
