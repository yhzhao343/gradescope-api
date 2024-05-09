from bs4 import BeautifulSoup

from gradescopeapi._classes._scrape_helpers import scrape_courses_info


class Account:
    def __init__(self, session):
        self.session = session

    def get_courses(self) -> dict:
        """
        Get all courses for the user, including both instructor and student courses

        Returns:
            dict: A dictionary of dictionaries, where keys are "instructor" and "student" and values are
            dictionaries containing all courses, where keys are course IDs and values are Course objects.

            For example:
                {
                'instructor': {
                    "123456": Course(...),
                    "234567": Course(...)
                },
                'student': {
                    "654321": Course(...),
                    "765432": Course(...)
                }
                }

        Raises:
            RuntimeError: If request to account page fails.
        """

        endpoint = "https://www.gradescope.com/account"

        # get main page
        response = self.session.get(endpoint)

        if response.status_code != 200:
            raise RuntimeError(
                "Failed to access account page on Gradescope. Status code: {response.status_code}"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        # see if user is solely a student or instructor
        user_courses, is_instructor = scrape_courses_info(
            self.session, soup, "Your Courses"
        )

        # if the user is indeed solely a student or instructor
        # return the appropriate set of courses
        if user_courses:
            if is_instructor:
                return {"instructor": user_courses, "student": {}}
            else:
                return {"instructor": {}, "student": user_courses}

        # if user is both a student and instructor, get both sets of courses
        courses = {"instructor": {}, "student": {}}

        # get instructor courses
        instructor_courses, _ = scrape_courses_info(
            self.session, soup, "Instructor Courses"
        )
        courses["instructor"] = instructor_courses

        # get student courses
        student_courses, _ = scrape_courses_info(self.session, soup, "Student Courses")
        courses["student"] = student_courses

        return courses
