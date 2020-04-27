from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now, timedelta
from exercises.forms import (
    SubmissionForm,
    REQUIRED_ERROR,
    EXTENSION_ERROR,
    MIME_ERROR,
    MIN_SIZE_ERROR,
    MAX_SIZE_ERROR,
)
from exercises.models import Exercise, Submission


PYTHON_MOCK = """
def hello_world(x):
    for i in range(x):
        print("Hello World!")
    return True
    """

PDF_MOCK = """
%PDF-1.1
%¥±ë

1 0 obj
  << /Type /Catalog
     /Pages 2 0 R
  >>
endobj
"""


class SubmissionFormTest(TestCase):

    def test_can_not_save_submission_without_file(self):
        exercise = Exercise.objects.create(number=1)
        submission = Submission(exercise=exercise)

        form = SubmissionForm(files={}, instance=submission)

        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_can_not_save_small_files(self):
        exercise = Exercise.objects.create(number=1)
        submission = Submission(exercise=exercise)
        file = SimpleUploadedFile("test.py", str.encode("import numpy as np"))

        form = SubmissionForm(files={'file': file}, instance=submission)

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors.keys())
        self.assertEqual(form.errors["file"], [MIN_SIZE_ERROR])
        with self.assertRaises(ValueError):
            form.save()

    def test_can_not_save_wrong_extension(self):
        exercise = Exercise.objects.create(number=1)
        submission = Submission(exercise=exercise)
        file = SimpleUploadedFile("cat.png", str.encode(PYTHON_MOCK))

        form = SubmissionForm(files={'file': file}, instance=submission)

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors.keys())
        self.assertEqual(form.errors["file"], [EXTENSION_ERROR])
        with self.assertRaises(ValueError):
            form.save()

    def test_can_not_save_wrong_mime_types(self):
        exercise = Exercise.objects.create(number=1)
        submission = Submission(exercise=exercise)
        file = SimpleUploadedFile("evil.py", str.encode(PDF_MOCK))

        form = SubmissionForm(files={'file': file}, instance=submission)

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors.keys())
        self.assertEqual(form.errors["file"], [MIME_ERROR])
        with self.assertRaises(ValueError):
            form.save()


class FileUploadTest(TestCase):

    def test_file_upload_works(self):
        exercise = Exercise.objects.create(number=1)
        file = SimpleUploadedFile("test.py", str.encode(PYTHON_MOCK))

        self.client.post(exercise.get_absolute_url(), {"file": file})

        self.assertEqual(Submission.objects.count(), 1)
        submission = Submission.objects.first()
        self.assertEqual(submission.exercise, exercise)
        self.assertEqual(submission.file.read(), str.encode(PYTHON_MOCK))

    def test_upload_of_wrong_mime(self):
        exercise = Exercise.objects.create(number=2)
        file = SimpleUploadedFile("test.py", str.encode(PDF_MOCK))

        response = self.client.post(exercise.get_absolute_url(), {'file': file})

        self.assertEqual(Submission.objects.count(), 0)
        self.assertContains(response, MIME_ERROR)

    def test_upload_of_wrong_extension(self):
        exercise = Exercise.objects.create(number=2)
        file = SimpleUploadedFile("test.png", str.encode(PYTHON_MOCK))

        response = self.client.post(exercise.get_absolute_url(), {'file': file})

        self.assertEqual(Submission.objects.count(), 0)
        self.assertContains(response, EXTENSION_ERROR)

    def test_upload_without_exercise(self):
        file = SimpleUploadedFile("test.png", str.encode(PYTHON_MOCK))

        self.client.post("/exercise/1/", data={"file": file})

        self.assertEqual(Submission.objects.count(), 0)

    def test_upload_of_not_released_exercise(self):
        file = SimpleUploadedFile("test.py", str.encode(PYTHON_MOCK))
        release = now() + timedelta(days=1)
        exercise = Exercise.objects.create(number=1, release=release)

        self.client.post(exercise.get_absolute_url(), data={"file": file})

        self.assertEqual(Submission.objects.count(), 0)

    def test_upload_of_expired_exercise(self):
        deadline = now() - timedelta(days=1)
        exercise = Exercise.objects.create(number=1, deadline=deadline)
        file = SimpleUploadedFile("test.py", b"...content...")

        self.client.post(exercise.get_absolute_url(), data={"file": file})

        self.assertEqual(Submission.objects.count(), 0)

    def test_invalid_upload_stays_on_same_page(self):
        exercise = Exercise.objects.create(number=2)
        file = SimpleUploadedFile("test.png", str.encode(PYTHON_MOCK))

        response = self.client.post(exercise.get_absolute_url(), {"file": file})

        self.assertTemplateUsed(response, "exercise.html")
        self.assertEqual(response.status_code, 200)

    def test_valid_upload_redirects_to_same_page(self):
        exercise = Exercise.objects.create(number=2)
        file = SimpleUploadedFile("test.py", str.encode(PYTHON_MOCK))

        response = self.client.post(exercise.get_absolute_url(), {"file": file})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], exercise.get_absolute_url())
