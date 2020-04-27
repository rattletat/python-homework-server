from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_navigate_to_exercise_page(self):
        # Student Lucy wants to start working on the second exercise.
        # She opens the exercise site.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention the course title.
        title = "Programmieren fuer Sozialwissenschaftler*innen"
        self.assertEqual(title, self.browser.title)
        header_text = self.browser.find_element_by_css_selector(".nav h1 a").text
        self.assertIn(title, header_text)

        # She sees a table with an old, a current
        # and a future programming exercise.
        table = self.browser.find_element_by_id("exercises")
        rows = table.find_elements_by_tag_name("tr")
        self.assertGreaterEqual(len(rows), 3)

        # She presses on the second link.
        # The page updates and now sees the lecture name in the header
        # and the exercise name in the subheader.
        link = self.get_exercise_link(2)
        self.browser.get(link)
        self.assertIn(title, self.get_title().text)
        self.assertIn("Programmieraufgabe 2", self.get_subtitle().text)

        # She sees that the assignment is open for submission
        status = self.get_status().text
        self.assertIn("Zur Abgabe bereit!", status)

        # She reads the well written description.
        description = self.get_description()
        self.assertIn("for-loop", description.text)
        self.assertNotIn("Hello World", description.text)

        # She navigates back to the home page by pressing on the header
        # and sees the exercises again
        header_link = self.browser.find_element_by_css_selector(".nav h1 a")
        self.browser.get(header_link.get_attribute('href'))
        table = self.browser.find_element_by_id("exercises")
