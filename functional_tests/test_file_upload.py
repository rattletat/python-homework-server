from .base import FunctionalTest
import os
from django.conf import settings


class UploadValidationTest(FunctionalTest):
    def test_can_upload_perfect_python_file(self):
        # Lucy worked on the problem.
        # Now she wants to submit it.
        # She navigates to Exercise 2
        self.browser.get(self.live_server_url)
        table = self.browser.find_element_by_id("exercises")
        active_row = table.find_element_by_id("active_exercise")
        url = active_row.find_element_by_tag_name("a").get_attribute("href")
        self.browser.get(url)

        # She sees the submission button and uploads a wrong Python file.
        upload_button = self.browser.find_element_by_id("id_file")
        fixture_path = os.path.join(settings.BASE_DIR, 'functional_tests/fixtures')
        upload_button.send_keys(os.path.join(fixture_path, 'wrong_homework.py'))

        # After a few seconds, she sees the score printed.
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("id_score").text, "50%"
            )
        )

        # She is shocked by the result and accidentally uploads an image
        upload_button.send_keys(os.path.join(fixture_path, 'cat.png'))
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text, "0%"
            )
        )

        # She notices her mistake and uploads the correct file
        upload_button.send_keys(os.path.join(fixture_path, 'correct_homework.py'))
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("score").text, "100%"
            )
        )
