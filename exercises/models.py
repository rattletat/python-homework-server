import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from .helper import (
    get_description_path,
    get_resources_path,
    get_submission_path,
    get_tests_path,
)
from .storage import OverwriteStorage
from .validators import FileValidator

FILE_MIN_SIZE = 30
FILE_MAX_SIZE = 5000


class Exercise(models.Model):
    number = models.PositiveSmallIntegerField(
        primary_key=True, validators=[MinValueValidator(1)],
    )
    short_name = models.CharField(max_length=50, null=True)
    release = models.DateTimeField(null=True, default=None)
    deadline = models.DateTimeField(null=True, default=None)
    description = models.FileField(
        storage=OverwriteStorage(),
        upload_to=get_description_path,
        validators=[
            FileValidator(
                allowed_mimetypes=["text/markdown", "text/plain", "text/x-python"],
                allowed_extensions=["md"],
            ),
        ],
    )
    tests = models.FileField(
        storage=OverwriteStorage(),
        upload_to=get_tests_path,
        validators=[
            FileValidator(
                allowed_mimetypes=["text/python", "text/x-python"], allowed_extensions=["py"],
            ),
        ],
    )
    max_tests = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    relevant = models.BooleanField("Fließt in die Wertung ein.", default=True)

    def get_absolute_url(self):
        return reverse("exercises:view_exercise", args=[self.number])

    def get_result_url(self):
        return reverse("exercises:view_results", args=[self.number])

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
        return f"Programmieraufgabe {self.number}: {self.short_name}"

    def clean(self):
        super().clean()

        if self.release and self.deadline and self.release > self.deadline:
            raise ValidationError(
                "Der Startzeitpunkt muss vor der Deadline liegen!", code="invalid_date",
            )

    class Meta:
        ordering = ("number",)


class ExerciseResource(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, editable=False)
    file = models.FileField(
        null=True, default=None, storage=OverwriteStorage(), upload_to=get_resources_path,
    )

    def clean(self):
        super().clean()

        basename = os.path.basename(self.file.name)
        reserved_files = ["runner.py", "submission.py", "tests.py"]
        if basename in reserved_files:
            raise ValidationError(
                f"Die Datei darf nicht einen der folgenden Namen haben: {str(reserved_files)}!",
                code="invalid_name",
            )


class Submission(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True, unique=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    file_hash = models.CharField(max_length=40, editable=False)
    file = models.FileField(
        upload_to=get_submission_path,
        validators=[
            FileValidator(
                min_size=FILE_MIN_SIZE,
                max_size=FILE_MAX_SIZE,
                allowed_mimetypes=["text/x-python", "text/plain"],
                allowed_extensions=["py"],
            ),
        ],
    )

    def __str__(self):
        try:
            return f"Submission on Exercise {self.exercise.number} by {self.user}, Punkte: {self.testresult}"
        except ObjectDoesNotExist:
            return f"Submission on Exercise {self.exercise.number} by {self.user}"

    class Meta:
        unique_together = (
            "file_hash",
            "user",
        )


class TestResult(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, editable=False,)
    processed = models.DateTimeField(auto_now_add=True, unique=True)
    job_id = models.CharField(max_length=128, editable=False)
    test_count = models.IntegerField(editable=False)
    success_count = models.IntegerField(editable=False)
    first_error = models.TextField(null=True, blank=True, editable=False)
    first_failure = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ("-processed",)

    def __str__(self):
        return f"{self.success_count}/{self.test_count}"
