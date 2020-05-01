from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib import auth

from exercises.models import Exercise, Submission

User = auth.get_user_model()


class ExerciseModelTest(TestCase):

    def test_default_description(self):
        exercise = Exercise(number=1)
        self.assertEqual(exercise.description, None)

    def test_default_release(self):
        exercise = Exercise(number=1)
        self.assertEqual(exercise.release, None)

    def test_default_deadline(self):
        exercise = Exercise(number=1)
        self.assertEqual(exercise.deadline, None)

    def test_get_absolute_url(self):
        exercise = Exercise.objects.create(number=7)
        self.assertEqual(exercise.get_absolute_url(), f"/exercise/{exercise.number}/")

    def test_exercise_released_status(self):
        release = now() - timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            self.assertTrue(exercise.released())

    def test_exercise_expired_status(self):
        release = now() - timedelta(days=2)
        deadline = now() - timedelta(days=1)
        Exercise.objects.create(number=2, deadline=deadline)
        Exercise.objects.create(number=3, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            self.assertTrue(exercise.expired())

    def test_exercise_not_released_status(self):
        release = now() + timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)
        for exercise in Exercise.objects.all():
            self.assertFalse(exercise.released())
            self.assertFalse(exercise.expired())

    def test_duplicate_excercises_are_invalid(self):
        Exercise.objects.create(number=1)
        with self.assertRaises(ValidationError):
            Exercise(number=1).full_clean()

    def test_exercise_cannot_have_number_zero(self):
        # FieldSmallNumberField includes 0
        with self.assertRaises(ValidationError):
            Exercise(number=0).full_clean()

    def test_exercise_cannot_have_negative_number(self):
        with self.assertRaises(ValidationError):
            Exercise(number=-1).full_clean()


class SubmissionModelTest(TestCase):

    def test_submission_is_related_to_exercise(self):
        exercise = Exercise.objects.create(number=1)
        user = User.objects.create(email="a@b.com")
        submission = Submission(exercise=exercise, user=user)
        submission.save()
        self.assertIn(submission, exercise.submission_set.all())
