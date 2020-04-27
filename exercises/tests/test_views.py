from django.test import TestCase
from exercises.models import Exercise
from django.utils.timezone import timedelta, now
from exercises.forms import SubmissionForm


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_released_exercise_has_valid_link(self):
        release = now() - timedelta(days=1)
        exercise = Exercise.objects.create(number=1, release=release)

        response = self.client.get("/")

        self.assertContains(response, ">1<")
        self.assertContains(response, f'href="{exercise.get_absolute_url()}"')

    def test_not_released_exercise_has_no_link(self):
        response = self.client.get("/")
        release = now() + timedelta(days=1)
        exercise = Exercise.objects.create(number=1, release=release)

        response = self.client.get("/")

        self.assertNotContains(response, f'href="{exercise.get_absolute_url()}"')

    def test_no_exercise_subheader(self):
        response = self.client.get("/")

        self.assertContains(response, ">Keine Programmieraufgaben!<")

    def test_multiple_exercises_subheader(self):
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2)

        response = self.client.get("/")

        self.assertContains(response, ">Programmieraufgaben:<")

    def test_no_exercise_table_not_shown(self):
        response = self.client.get("/")

        self.assertNotContains(response, 'id="table-header"')


class ExerciseViewTest(TestCase):
    def test_exercise_links_give_correct_html(self):
        exercise = Exercise.objects.create(number=1)
        response = self.client.get(exercise.get_absolute_url())
        self.assertTemplateUsed(response, "exercise.html")

    def test_exercise_view_shows_correct_number(self):
        exercise = Exercise.objects.create(number=7)
        response = self.client.get(exercise.get_absolute_url())
        self.assertContains(response, "Programmieraufgabe 7")

    def test_active_exercise_view_shows_correct_status(self):
        release = now() - timedelta(days=1)
        deadline = now() + timedelta(days=1)
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)
        Exercise.objects.create(number=4, deadline=deadline)

        for exercise in Exercise.objects.all():
            response = self.client.get(exercise.get_absolute_url())
            self.assertContains(response, "Zur Abgabe bereit!")
            self.assertNotContains(response, "Nicht veröffentlicht!")

    def test_active_exercise_view_shows_correct_form(self):
        release = now() - timedelta(days=1)
        deadline = now() + timedelta(days=1)
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)
        Exercise.objects.create(number=4, deadline=deadline)

        for exercise in Exercise.objects.all():
            response = self.client.get(exercise.get_absolute_url())
            self.assertIsInstance(response.context['form'], SubmissionForm)

    def test_expired_exercise_view_shows_correct_status(self):
        release = now() - timedelta(days=2)
        deadline = now() - timedelta(days=1)
        Exercise.objects.create(number=1, deadline=deadline)
        Exercise.objects.create(number=2, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            response = self.client.get(exercise.get_absolute_url())
            self.assertContains(response, "Abgabe beendet!")
            self.assertNotContains(response, "Nicht veröffentlicht!")
            self.assertNotContains(response, "Zur Abgabe bereit!")

    def test_expired_exercise_does_not_show_form(self):
        release = now() - timedelta(days=2)
        deadline = now() - timedelta(days=1)
        Exercise.objects.create(number=1, deadline=deadline)
        Exercise.objects.create(number=2, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            response = self.client.get(exercise.get_absolute_url())
            self.assertNotIn('form', response)

    def test_waiting_exercise_does_not_show_exercise_view(self):
        release = now() + timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=1, release=release)
        Exercise.objects.create(number=2, release=release, deadline=deadline)

        for exercise in Exercise.objects.all():
            response = self.client.get(exercise.get_absolute_url())
            self.assertTemplateNotUsed(response, "exercise.html")

    def test_exercise_page_shows_correct_description(self):
        correct_description = "Please write a simple Hello World program!"
        wrong_description = "Double Rainbow all the way!"
        Exercise.objects.create(number=1, description=wrong_description)
        exercise = Exercise.objects.create(number=2, description=correct_description)
        Exercise.objects.create(number=3, description=wrong_description)
        response = self.client.get(exercise.get_absolute_url())
        self.assertNotContains(response, wrong_description)
        self.assertContains(response, correct_description)

    def test_exercise_view_uses_submission_form(self):
        exercise = Exercise.objects.create(number=1)
        response = self.client.get(exercise.get_absolute_url())
        self.assertIsInstance(response.context["form"], SubmissionForm)

    def test_exercise_view_shows_description(self):
        exercise = Exercise.objects.create(number=1, description="Coffee")
        response = self.client.get(exercise.get_absolute_url())
        self.assertContains(response, "Coffee")

    def test_exercise_view_renders_markdown(self):
        exercise = Exercise.objects.create(number=1, description="**Coffee**")
        response = self.client.get(exercise.get_absolute_url())
        self.assertContains(response, "<strong>Coffee</strong>")
