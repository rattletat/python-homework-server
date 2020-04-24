from django.test import TestCase
from exercises.models import Exercise
from django.utils.timezone import timedelta, now


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_started_exercise_has_valid_link(self):
        release = now() - timedelta(days=1)
        Exercise.objects.create(number=1, release=release)

        response = self.client.get("/")

        self.assertContains(response, ">1<")
        self.assertContains(response, 'href="/exercise/1/"')

    def test_not_started_exercise_has_no_link(self):
        response = self.client.get("/")
        release = now() + timedelta(days=1)
        Exercise.objects.create(number=1, release=release)

        response = self.client.get("/")

        self.assertNotContains(response, 'href="/exercise/1/"')

    def test_no_exercise_subheader(self):
        response = self.client.get("/")

        self.assertContains(response, "Keine Programmieraufgaben!")

    def test_one_exercise_subheader(self):

        Exercise.objects.create(number=1)

        response = self.client.get("/")

        self.assertContains(response, "Programmieraufgabe:")

    def test_many_exercises_subheader(self):
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2)

        response = self.client.get("/")

        self.assertContains(response, "Programmieraufgaben:")


class ExerciseTest(TestCase):
    def test_exercise_links_give_correct_html(self):
        exercise = Exercise.objects.create(number=1)
        response = self.client.get(f"/exercise/{exercise.number}/")
        self.assertTemplateUsed(response, "exercise.html")

    def test_exercise_page_shows_correct_number(self):
        exercise = Exercise.objects.create(number=7)
        response = self.client.get(f"/exercise/{exercise.number}/")
        self.assertContains(response, "Programmieraufgabe 7")
