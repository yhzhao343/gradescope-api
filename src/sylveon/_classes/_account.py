from bs4 import BeautifulSoup
import requests

from sylveon._classes._scrape_helpers import scrape_courses_info


class Account:

    def __init__(self, session):
        self.session = session

    def get_courses(self) -> dict:
        courses = {"instructor": {}, "student": {}}

        endpoint = "https://www.gradescope.com/account"

        # get main page
        response = self.session.get(endpoint)
        soup = BeautifulSoup(response.text, "html.parser")

        # get instructor courses
        instructor_courses = scrape_courses_info(
            self.session, soup, "Instructor Courses"
        )
        courses["instructor"] = instructor_courses

        # get student courses
        student_courses = scrape_courses_info(self.session, soup, "Student Courses")
        courses["student"] = student_courses

        return courses
