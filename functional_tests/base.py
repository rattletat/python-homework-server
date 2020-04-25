import os

from django.test import LiveServerTestCase
from django.utils.timezone import now, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from exercises.models import Exercise


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        # Database setup
        self.setup_database()

        # Browser options
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

        # Live test
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def setup_database(self):
        # Past exercise
        Exercise.objects.create(
            number=1,
            release=now() - timedelta(days=10),
            deadline=now() - timedelta(days=3),
            description="Please print `Hello World` to standard output."
        )
        # Current exercise
        Exercise.objects.create(
            number=2,
            release=now() - timedelta(days=3),
            deadline=now() + timedelta(days=4),
            description="Please construct a simple for-loop."
        )
        # Future exercise
        Exercise.objects.create(
            number=3,
            release=now() + timedelta(days=4),
            deadline=now() + timedelta(days=11),
            description="Please code a recursive metaclass-based polymorphic tree parser factory."
        )
