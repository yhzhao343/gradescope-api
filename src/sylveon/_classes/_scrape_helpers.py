from bs4 import BeautifulSoup
import requests


def scrape_courses_info(
    session: requests.Session, soup: BeautifulSoup, user_type: str
) -> dict:
    # find heading for defined user_type's courses
    courses = soup.find("h1", class_="pageHeading", text=user_type)

    all_courses = {}
    if courses is not None:
        # find next div with class courseList
        course_list = courses.find_next("div", class_="courseList")
        for semester in course_list.find_all("div", class_="courseList--term"):
            # find first "a" -> course
            course = semester.find_next("a")
            while course is not None:
                course_info = {}
                # fetch course id and create new dictionary for each course
                course_id = course["href"].split("/")[-1]

                # fetch short name
                course_name = course.find("h3", class_="courseBox--shortname")
                course_info["short_name"] = course_name.text

                # fetch full name
                course_full_name = course.find("div", class_="courseBox--name")
                course_info["full_name"] = course_full_name.text

                # fetch semester and year
                time_of_year = semester.text.split(" ")
                course_info["semester"] = time_of_year[0]
                course_info["year"] = time_of_year[1]

                # fetch number of grades published and number of assignments
                if user_type == "Instructor Courses":
                    num_grades_published = course.find(
                        "div", class_="courseBox--noGradesPublised"
                    )
                    course_info["num_grades_published"] = num_grades_published.text
                    num_assignments = course.find(
                        "div",
                        class_="courseBox--assignments courseBox--assignments-unpublished",
                    )
                    course_info["num_assignments"] = num_assignments.text
                else:
                    num_assignments = course.find(
                        "div", class_="courseBox--assignments"
                    )
                    course_info["num_assignments"] = num_assignments.text

                # store info for this course
                all_courses[course_id] = course_info

                # find next course, or "a" tag
                course = course.find_next_sibling("a")

        return all_courses
