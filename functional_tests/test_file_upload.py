from .base import FunctionalTest


class UploadValidationTest(FunctionalTest):
    def test_can_upload_perfect_python_file(self):
        # Lucy worked on the problem.
        # Now she wants to submit it.
        # She navigates to Exercise 2
        self.browser.get(self.live_server_url)
        link = self.get_exercise_link(2)
        self.browser.get(link)

        # She sees the submission button and uploads a wrong Python file.
        # After a few seconds, she sees the score printed.
        upload_button = self.get_upload_button()
        upload_button.send_keys(self.get_fixture('wrong_homework.py'))
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("id_score").text, "50%"
            )
        )

        # She is shocked by the result and accidentally uploads an image
        upload_button = self.get_upload_button()
        upload_button.send_keys(self.get_fixture('cat.png'))
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text, "0%"
            )
        )

        # She notices her mistake and uploads the correct file
        upload_button = self.get_upload_button()
        upload_button.send_keys(self.get_fixture('correct_homework.py'))
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("score").text, "100%"
            )
        )
