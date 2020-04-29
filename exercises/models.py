from django.db import models
from django.urls import reverse
from exercises.validators import FileValidator
from django.utils.timezone import now
from django.core.validators import MinValueValidator

FILE_MIN_SIZE = 30
FILE_MAX_SIZE = 3000


def _user_directory_path(obj, _):
    if isinstance(obj, Submission):
        timestamp = obj.uploaded.strftime("%d-%m-%Y_%H-%M-%S")
        return f"submission/test_user/{obj.exercise.number}/{timestamp}.py"
    elif isinstance(obj, Exercise):
        return f"exercise/{obj.exercise.number}/description.md"


class Exercise(models.Model):
    number = models.PositiveSmallIntegerField(
        primary_key=True, default=None, validators=[MinValueValidator(1)]
    )
    release = models.DateTimeField(null=True, default=None)
    deadline = models.DateTimeField(null=True, default=None)
    description = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse("exercise:view_exercise", args=[self.number])

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

    class Meta:
        ordering = ("number",)


class Submission(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True, unique=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    file = models.FileField(
        upload_to=_user_directory_path,
        validators=[
            FileValidator(
                min_size=FILE_MIN_SIZE,
                max_size=FILE_MAX_SIZE,
                allowed_mimetypes=["text/x-python"],
                allowed_extensions=["py"],
            )
        ],
    )
