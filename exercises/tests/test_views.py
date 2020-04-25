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

    def test_no_exercise_table_not_shown(self):
        response = self.client.get("/")

        self.assertNotContains(response, 'id="table-header"')

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
        Exercise.objects.create(number=1)
        response = self.client.get("/exercise/1/")
        self.assertTemplateUsed(response, "exercise.html")

    def test_exercise_page_shows_correct_number(self):
        Exercise.objects.create(number=7)
        response = self.client.get(f"/exercise/7/")
        self.assertContains(response, "Programmieraufgabe 7")

    def test_active_exercise_page_shows_correct_status(self):
        release = now() - timedelta(days=1)
        deadline = now() + timedelta(days=1)
        Exercise.objects.create(number=1)
        Exercise.objects.create(number=2, release=release)
        Exercise.objects.create(number=3, release=release, deadline=deadline)
        Exercise.objects.create(number=4, deadline=deadline)

        for i, _ in enumerate(Exercise.objects.all(), start=1):
            response = self.client.get(f"/exercise/{i}/")
            self.assertContains(response, "Zur Abgabe bereit!")

    def test_waiting_exercise_does_not_exist(self):
        release = now() + timedelta(days=1)
        deadline = now() + timedelta(days=2)
        Exercise.objects.create(number=1, release=release)
        Exercise.objects.create(number=2, release=release, deadline=deadline)
        response_1 = self.client.get("/exercise/1/")
        self.assertTemplateNotUsed(response_1, "exercise.html")
        response_2 = self.client.get("/exercise/2/")
        self.assertTemplateNotUsed(response_2, "exercise.html")

    def test_expired_exercise_page_shows_correct_status(self):
        release = now() - timedelta(days=2)
        deadline = now() - timedelta(days=1)
        Exercise.objects.create(number=1, deadline=deadline)
        Exercise.objects.create(number=2, release=release, deadline=deadline)

        for i, _ in enumerate(Exercise.objects.all(), start=1):
            response = self.client.get(f"/exercise/{i}/")
            self.assertContains(response, "Abgabe beendet!")

    def test_exercise_page_shows_correct_description(self):
        correct_description = "Please write a simple Hello World program!"
        wrong_description = "Double Rainbow all the way!"
        Exercise.objects.create(number=1, description=wrong_description)
        Exercise.objects.create(number=2, description=correct_description)
        Exercise.objects.create(number=3, description=wrong_description)
        response = self.client.get("/exercise/2/")
        self.assertNotContains(response, wrong_description)
        self.assertContains(response, correct_description)

    # def test_exercise_file_upload_possible(self):
    #     release = now() - timedelta(days=1)
    #     deadline = now() + timedelta(days=1)
    #     Exercise.objects.create(number=1)
    #     Exercise.objects.create(number=2, release=release)
    #     Exercise.objects.create(number=3, release=release, deadline=deadline)
    #     Exercise.objects.create(number=4, deadline=deadline)

    #     for ix, _ in enumerate(Exercise.objects.all(), start=1):
    #         self.client.get(f'/exercise/{ix}/')
    #         # upload_button = self.client.find_element_by_id('submission')
    #         # upload_button.send_keys('/functional_tests/rsc/homework_1.py')
