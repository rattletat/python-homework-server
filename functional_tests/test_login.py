from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'rattletat@posteo.me'
SUBJECT = "Dein Login Link für 'Programmieren für Sozialwissenschaftler*innen'"


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Dein Login Link ist soeben in deinem Email Postfach angekommen.',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Benutze diesen Link um dich auf der Seite einzuloggen', email.body)
        url_search = re.search('http://.+/.+', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.assertIn(TEST_EMAIL, self.browser.page_source)
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out').click()
        )

        # she is logged out!
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        self.assertNotIn(TEST_EMAIL, self.browser.page_source)
