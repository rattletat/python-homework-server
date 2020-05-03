from django.db import models
from django.urls import reverse
from .utils import get_submission_dir
from django.core.exceptions import ValidationError
from exercises.validators import FileValidator
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.conf import settings

FILE_MIN_SIZE = 30
FILE_MAX_SIZE = 3000


class Exercise(models.Model):
    number = models.PositiveSmallIntegerField(
        primary_key=True, default=None, validators=[MinValueValidator(1)]
    )
    release = models.DateTimeField(null=True, default=None)
    deadline = models.DateTimeField(null=True, default=None)
    description = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse("exercises:view_exercise", args=[self.number])

    def released(self):
        if self.release:
            return self.release < now()
        else:
            return True

    def expired(self):
        if self.deadline:
            return self.deadline < now()
        else:
            return False

    def __str__(self):
        return f"Programmieraufgabe {self.number}"

    def clean(self):
        super().clean()

        if self.release > self.deadline:
            raise ValidationError("Der Startzeitpunkt muss vor der Deadline liegen!", code="invalid_date")

    class Meta:
        ordering = ("number",)


class Submission(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True, unique=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    file_hash = models.CharField(max_length=40, editable=False)
    file = models.FileField(
        upload_to=get_submission_dir,
        validators=[
            FileValidator(
                min_size=FILE_MIN_SIZE,
                max_size=FILE_MAX_SIZE,
                allowed_mimetypes=["text/x-python", "text/plain"],
                allowed_extensions=["py"],
            ),
        ],
    )

    class Meta:
        unique_together = ('file_hash', 'user',)
