from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils.timezone import now, timedelta

from exercises.models import Exercise


class ExerciseModelTest(TestCase):
    def test_exercise_released(self):
        release = now() - timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            self.assertTrue(exercise.released())

    def test_exercise_expired(self):
        release = now() - timedelta(days=2)
        deadline = now() - timedelta(days=1)
        Exercise.objects.create(number=2, deadline=deadline)
        Exercise.objects.create(number=3, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            self.assertTrue(exercise.expired())

    def test_exercise_not_released(self):
        release = now() + timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)
        for exercise in Exercise.objects.all():
            self.assertFalse(exercise.released())
            self.assertFalse(exercise.expired())

    def test_exercise_number_are_unique(self):
        Exercise.objects.create(number=7)
        # Tests are atomic by default.
        # Therefore atomic() is needed to suppress TransactionError.
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Exercise.objects.create(number=7)
        self.assertEqual(Exercise.objects.count(), 1)

    def test_exercise_can_only_have_strictly_positive_number(self):
        # FieldSmallNumberField includes 0
        with self.assertRaises(ValidationError):
            Exercise(number=0).full_clean()
            Exercise.objects.create(number=0)

        with self.assertRaises(ValidationError):
            Exercise(number=-1).full_clean()

        with self.assertRaises(IntegrityError):
            Exercise.objects.create(number=-1)

    def test_get_absolute_url(self):
        exercise = Exercise.objects.create(number=7)
        self.assertEqual(exercise.get_absolute_url(), f"/exercise/{exercise.number}/")
