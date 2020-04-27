from django import forms
from exercises.models import Submission
from exercises.models import FILE_MIN_SIZE, FILE_MAX_SIZE

REQUIRED_ERROR = "Du musst eine Datei hochladen!"
EXTENSION_ERROR = "Deine Datei muss eine .py Dateiendung haben!"
MIME_ERROR = "Du musst eine valide Python Datei hochladen!"
MIN_SIZE_ERROR = f"Deine Datei muss mindestens {FILE_MIN_SIZE}B groß sein!"
MAX_SIZE_ERROR = f"Deine Datei muss kleiner als {FILE_MAX_SIZE}B sein!"


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
            }
        }

    def save(self, exercise):
        self.instance.exercise = exercise
        return super().save()
