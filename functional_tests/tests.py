import os

from django.test import LiveServerTestCase
from django.utils.timezone import now, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.conf import settings


from exercises.models import Exercise


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        # Past exercise
        Exercise.objects.create(
            number=1,
            release=now() - timedelta(days=10),
            deadline=now() - timedelta(days=3),
        )
        # Current exercise
        Exercise.objects.create(
            number=2,
            release=now() - timedelta(days=3),
            deadline=now() + timedelta(days=4),
        )
        # Future exercise
        Exercise.objects.create(
            number=3,
            release=now() + timedelta(days=4),
            deadline=now() + timedelta(days=11),
        )

    def tearDown(self):
        self.browser.quit()

    def test_can_navigate_to_exercise_page(self):
        # Student Lucy wants to start working on the second exercise.
        # She opens the exercise site.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention the course title.
        title = "Programmieren für Sozialwissenschaftler*innen"
        self.assertIn(title, self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn(title, header_text)

        # She sees a table with an old, a current
        # and a future programming exercise.
        table = self.browser.find_element_by_id('id_exercises')
        rows = table.find_elements_by_tag_name('tr')
        print(settings.DEBUG)
        print(settings.STATIC_ROOT)
        self.assertGreaterEqual(len(rows), 3)

        # She presses on the link of the active exercise.
        # The page updates and now sees the lecture name in the header
        # and the exercise name in the subheader.
        active_row = table.find_element_by_id("id_active_exercise")
        exercise_link = active_row.find_element_by_tag_name("a")
        exercise_link.click()
        header_text = self.browser.find_element_by_tag_name("h1").text
        subheader_text = self.browser.find_element_by_tag_name("small").text
        self.assertIn(title, header_text)
        self.assertIn("Programmieraufgabe 2", subheader_text)
