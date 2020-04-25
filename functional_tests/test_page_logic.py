from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_navigate_to_exercise_page(self):
        # Student Lucy wants to start working on the second exercise.
        # She opens the exercise site.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention the course title.
        title = "Programmieren für Sozialwissenschaftler*innen"
        self.assertIn(title, self.browser.title)
        header_text = self.browser.find_element_by_css_selector(".nav h1 a").text
        self.assertIn(title, header_text)

        # She sees a table with an old, a current
        # and a future programming exercise.
        table = self.browser.find_element_by_id("exercises")
        rows = table.find_elements_by_tag_name("tr")
        self.assertGreaterEqual(len(rows), 3)

        # She presses on the link of the active exercise.
        # The page updates and now sees the lecture name in the header
        # and the exercise name in the subheader.
        active_row = table.find_element_by_id("active_exercise")
        link = active_row.find_element_by_tag_name("a")
        self.browser.get(link.get_attribute("href"))
        header = self.browser.find_element_by_css_selector(".nav h1 a").text
        subheader = self.browser.find_element_by_css_selector(".nav h1 small").text
        self.assertIn(title, header)
        self.assertIn("Programmieraufgabe 2", subheader)

        # She sees that the assignment is open for submission
        status = self.browser.find_element_by_id("status").text
        self.assertIn("Zur Abgabe bereit!", status)

        # She reads the well written description.
        description = self.browser.find_element_by_id("description").text
        self.assertIn("for-loop", description)
        self.assertNotIn("Hello World", description)
