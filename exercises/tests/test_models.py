from exercises.models import Exercise
from django.utils.timezone import timedelta, now
from django.test import TestCase


class ExerciseModelTest(TestCase):
    def test_exercise_started(self):
        release = now() - timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            self.assertTrue(exercise.is_started())

    def test_exercise_expired(self):
        release = now() - timedelta(days=2)
        deadline = now() - timedelta(days=1)
        Exercise.objects.create(number=2, deadline=deadline)
        Exercise.objects.create(number=3, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            self.assertTrue(exercise.is_expired())

    def test_exercise_not_started(self):
        release = now() + timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)
        for exercise in Exercise.objects.all():
            self.assertFalse(exercise.is_started())
            self.assertFalse(exercise.is_expired())
