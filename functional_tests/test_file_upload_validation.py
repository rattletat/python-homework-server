import time
from unittest import skip

from .base import FunctionalTest


class UploadValidationTest(FunctionalTest):

    @skip
    def test_can_upload_perfect_python_file(self):
        # Lucy worked on the problem.
        # Now she wants to submit it.
        # She navigates to Exercise 2
        self.browser.get(self.live_server_url)
        table = self.browser.find_element_by_id('exercises')
        active_row = table.find_element_by_id("active_exercise")
        url = active_row.find_element_by_tag_name("a").get_attribute('href')
        self.browser.get(url)

        # She sees the submission button and uploads a Python file.
        upload_button = self.browser.find_element_by_id('submission')
        upload_button.send_keys('/functional_tests/rsc/homework_1.py')

        # After a few seconds, she sees the score printed.
        time.sleep(5)
        score = self.browser.find_element_by_id('score')
        self.assertIn('100%', score.text)
