from bs4 import BeautifulSoup
from typing import List, Dict

from gradescopeapi._classes._scrape_helpers import scrape_courses_info
from gradescopeapi._classes._assignment_helpers import (
    check_page_auth,
    get_assignments_instructor_view,
    get_assignments_student_view,
)


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
    
    def get_assignments(self, course_id: int) -> List[Dict[str, str]]:
        """
        Get a list of detailed assignment information for a course
        Returns:
            list: A list of dictionaries, where the keys are the assignment info name and
            the values is the corresponding assignment information
            Example:
                [
                   {
                        'assignment_id': 'a_id',
                        'name': 'a_name,
                        'release_date': 'a_release_date',
                        'due_date': 'a_due_date',
                        'late_due_date': 'a_late_due_date',
                        'submissions_status': 'a_status',
                        'grade': 'a_grade',
                        'max_grade': 'a_max_grade'
                   }
                ]
        Raises:
            Exceptions:
            "One or more invalid parameters": if course_id or assignment_id is null or empty value
            "You are not authorized to access this page.": if logged in user is unable to access submissions
            "You must be logged in to access this page.": if no user is logged in
        """
        ACCOUNT_PAGE_ENDPOINT = "https://www.gradescope.com/courses"
        course_endpoint = f"{ACCOUNT_PAGE_ENDPOINT}/{course_id}"
        # check that course_id is valid (not empty)
        if not course_id:
            raise Exception("Invalid Course ID")
        session = self.session
        # scrape page
        coursepage_resp = check_page_auth(session, course_endpoint)
        coursepage_soup = BeautifulSoup(coursepage_resp.text, "html.parser")

        # two different helper functions to parse assignment info
        # webpage html structure differs based on if user if instructor or student
        assignment_info_list = get_assignments_instructor_view(coursepage_soup)
        if not assignment_info_list:
            assignment_info_list = get_assignments_student_view(coursepage_soup)

        return assignment_info_list