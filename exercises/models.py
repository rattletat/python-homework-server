from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from exercises.helper import (get_description_path, get_submission_path,
                              get_tests_path)
from exercises.storage import OverwriteStorage
from exercises.validators import FileValidator

FILE_MIN_SIZE = 30
FILE_MAX_SIZE = 3000


class Exercise(models.Model):
    number = models.PositiveSmallIntegerField(
        primary_key=True, default=None, validators=[MinValueValidator(1)]
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
                allowed_mimetypes=["text/python", "text/x-python"],
                allowed_extensions=["py"],
            ),
        ],
    )

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
        return f"Programmieraufgabe {self.number}: {self.short_name}"

    def clean(self):
        super().clean()

        if self.release and self.deadline and self.release > self.deadline:
            raise ValidationError(
                "Der Startzeitpunkt muss vor der Deadline liegen!", code="invalid_date"
            )

    class Meta:
        ordering = ("number",)


class Submission(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True, unique=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
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

    class Meta:
        unique_together = (
            "file_hash",
            "user",
        )


class TestResult(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    processed = models.DateTimeField(auto_now_add=True, unique=True)
    job_id = models.CharField(max_length=128)
    test_count = models.IntegerField()
    success_count = models.IntegerField()

    class Meta:
        ordering = ("-processed",)


class TestMessage(models.Model):
    test = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    message = models.TextField(default=None)
    # Errors are raised because of structural faults, failures due to functional faults
    kind = models.CharField(
        choices=[("error", "Error"), ("failure", "Failure")], max_length=8
    )
