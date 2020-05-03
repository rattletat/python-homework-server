from django import forms
from .utils import generate_sha1
from django.core.exceptions import ValidationError
from exercises.models import Submission
from exercises.models import FILE_MIN_SIZE, FILE_MAX_SIZE

REQUIRED_ERROR = "Du musst eine Datei hochladen!"
EXTENSION_ERROR = "Deine Datei muss eine .py Dateiendung haben!"
MIME_ERROR = "Du musst eine valide Python Datei hochladen!"
MIN_SIZE_ERROR = f"Deine Datei muss mindestens {FILE_MIN_SIZE}B groß sein!"
MAX_SIZE_ERROR = f"Deine Datei muss kleiner als {FILE_MAX_SIZE}B sein!"
DUPLICATE_ERROR = "Diese Datei hast du schon zuvor hochgeladen!"
EXPIRED_ERROR = "Die Programmieraufgabe ist leider abgelaufen!"
NOT_RELEASED_ERROR = "Die Programmieraufgabe ist noch nicht zur Abgabe freigegeben!"


class SubmissionForm(forms.models.ModelForm):
    class Meta:
        model = Submission
        fields = ("file",)
        widget = {"file": forms.FileField()}
        error_messages = {
            "file": {
                "required": REQUIRED_ERROR,
                "extension": EXTENSION_ERROR,
                "mime": MIME_ERROR,
                "min_size": MIN_SIZE_ERROR,
                "max_size": MAX_SIZE_ERROR,
                "expired": EXPIRED_ERROR,
                "not_released": NOT_RELEASED_ERROR,
                "test": MIME_ERROR,
            }
        }

    def clean(self):
        super().clean()
        hash = generate_sha1(self.cleaned_data["file"])
        try:
            Submission.objects.get(file_hash=hash, user=self.instance.user)
        except Submission.DoesNotExist:
            self.instance.file_hash = hash
        else:
            raise ValidationError(DUPLICATE_ERROR)

        if not self.instance.exercise.released():
            raise ValidationError(NOT_RELEASED_ERROR)

        if self.instance.exercise.expired():
            raise ValidationError(EXPIRED_ERROR)
