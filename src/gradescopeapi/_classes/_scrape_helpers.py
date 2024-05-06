from bs4 import BeautifulSoup
import requests
from gradescopeapi._classes._courses import Course


def scrape_courses_info(
    session: requests.Session, soup: BeautifulSoup, user_type: str
) -> tuple[dict[str, Course], bool]:
    """
    Scrape all course info from the main page of Gradescope.

    Args:
        session (requests.Session): The session object used for making HTTP requests.
        soup (BeautifulSoup): BeautifulSoup object with parsed HTML.
        user_type (str): The user type to scrape courses for (Instructor or Student courses).

    Returns:
        tuple:
            dict: A dictionary mapping course IDs to Course objects containing all course info.
            bool: Flag indicating if the user is an instructor or not.

        For example:
        {
            "123456": Course(
                name="CS 1134",
                full_name="Data Structures and Algorithms",
                semester="Fall",
                year="2021",
                num_grades_published="0",
                num_assignments="5"
            )
        }
    """

    # initalize dictionary to store all courses
    all_courses = {}

    # find heading for defined user_type's courses
    courses = soup.find("h1", class_="pageHeading", string=user_type)

    # if no courses found, return empty dictionary
    if courses is None:
        return all_courses, False

    # use button to check if user is an instructor or not
    button = courses.find_next("button")
    if button.text == " Create a new course":  # intentional space before Create
        is_instructor = True
    else:
        is_instructor = False

    # find next div with class courseList
    course_list = courses.find_next("div", class_="courseList")

    for term in course_list.find_all("div", class_="courseList--term"):
        # find first "a" -> course
        course = term.find_next("a")
        while course is not None:
            # fetch course id and create new dictionary for each course
            course_id = course["href"].split("/")[-1]

            # fetch short name
            course_name = course.find("h3", class_="courseBox--shortname")
            short_name = course_name.text

            # fetch full name
            course_full_name = course.find("div", class_="courseBox--name")
            full_name = course_full_name.text

            # fetch semester and year
            time_of_year = term.text.split(" ")
            semester = time_of_year[0]
            year = time_of_year[1]

            # fetch number of grades published and number of assignments
            if user_type == "Instructor Courses" or is_instructor:
                num_grades_published = course.find(
                    "div", class_="courseBox--noGradesPublised"
                )
                num_grades_published = num_grades_published.text
                num_assignments = course.find(
                    "div",
                    class_="courseBox--assignments courseBox--assignments-unpublished",
                )
                num_assignments = num_assignments.text
            else:
                # students do not have number of grades published, so set to None
                num_grades_published = None
                num_assignments = course.find("div", class_="courseBox--assignments")
                num_assignments = num_assignments.text

            # create Course object with all relevant info
            course_info = Course(
                name=short_name,
                full_name=full_name,
                semester=semester,
                year=year,
                num_grades_published=num_grades_published,
                num_assignments=num_assignments,
            )

            # store info for this course
            all_courses[course_id] = course_info

            # find next course, or "a" tag
            course = course.find_next_sibling("a")

    return all_courses, is_instructor
