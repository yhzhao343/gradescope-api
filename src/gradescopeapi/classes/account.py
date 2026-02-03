from math import trunc
import time

from bs4 import BeautifulSoup

from gradescopeapi import DEFAULT_GRADESCOPE_BASE_URL
from gradescopeapi.classes._helpers._assignment_helpers import (
    check_page_auth,
    get_assignments_instructor_view,
    get_assignments_student_view,
    get_submission_files,
    get_user_submission_info,
)
from gradescopeapi.classes._helpers._course_helpers import (
    get_course_members,
    get_courses_info,
)
from gradescopeapi.classes.assignments import Assignment
from gradescopeapi.classes.member import Member
import json
from datetime import datetime


class Account:
    def __init__(
        self,
        session,
        gradescope_base_url: str = DEFAULT_GRADESCOPE_BASE_URL,
    ):
        self.session = session
        self.gradescope_base_url = gradescope_base_url

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

        endpoint = f"{self.gradescope_base_url}/account"

        # get main page
        response = self.session.get(endpoint)

        if response.status_code != 200:
            raise RuntimeError(
                "Failed to access account page on Gradescope. Status code: {response.status_code}"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        # see if user is solely a student or instructor
        user_courses, is_instructor = get_courses_info(soup, "Your Courses")

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
        instructor_courses, _ = get_courses_info(soup, "Instructor Courses")
        courses["instructor"] = instructor_courses

        # get student courses
        student_courses, _ = get_courses_info(soup, "Student Courses")
        courses["student"] = student_courses

        return courses

    def get_course_users(self, course_id: str) -> list[Member]:
        """
        Get a list of all users in a course
        Returns:
            list: A list of users in the course (Member objects)
        Raises:
            Exceptions:
            "One or more invalid parameters": if course_id is null or empty value
            "You must be logged in to access this page.": if no user is logged in
        """

        membership_endpoint = (
            f"{self.gradescope_base_url}/courses/{course_id}/memberships"
        )

        # check that course_id is valid (not empty)
        if not course_id:
            raise Exception("Invalid Course ID")

        session = self.session

        try:
            # scrape page
            membership_resp = check_page_auth(session, membership_endpoint)
            membership_soup = BeautifulSoup(membership_resp.text, "html.parser")

            # get all users in the course
            users = get_course_members(membership_soup, course_id)

            return users
        except Exception:
            return None

    def get_assignments(self, course_id: str) -> list[Assignment]:
        """
        Get a list of detailed assignment information for a course
        Returns:
            list: A list of Assignments
        Raises:
            Exceptions:
            "One or more invalid parameters": if course_id or assignment_id is null or empty value
            "You are not authorized to access this page.": if logged in user is unable to access submissions
            "You must be logged in to access this page.": if no user is logged in
        """
        course_endpoint = f"{self.gradescope_base_url}/courses/{course_id}"
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

    def get_assignment_submissions(
        self, course_id: str, assignment_id: str
    ) -> dict[str, list[str]]:
        """
        Get a list of dicts mapping AWS links for all submissions to each submission id
        Returns:
            dict: A dictionary of submissions, where the keys are the submission ids and the values are
            a list of aws links to the submission pdf
            For example:
                {
                    'submission_id': [
                        'aws_link1.com',
                        'aws_link2.com',
                        ...
                    ],
                    ...
                }
        Raises:
            Exceptions:
                "One or more invalid parameters": if course_id or assignment_id is null or empty value
                "You are not authorized to access this page.": if logged in user is unable to access submissions
                "You must be logged in to access this page.": if no user is logged in
                "Page not Found": When link is invalid: change in url, invalid course_if or assignment id
                "Image only submissions not yet supported": assignment is image submission only, which is not yet supported
        NOTE:
        1. Image submissions not supports, need to find an endpoint to retrieve image pdfs
        2. Not recommended for use, since this makes a GET request for every submission -> very slow!
        3. so far only accessible for teachers, not for students to get submissions to an assignment
        """
        ASSIGNMENT_ENDPOINT = f"{self.gradescope_base_url}/courses/{course_id}/assignments/{assignment_id}"
        ASSIGNMENT_SUBMISSIONS_ENDPOINT = f"{ASSIGNMENT_ENDPOINT}/review_grades"
        if not course_id or not assignment_id:
            raise Exception("One or more invalid parameters")
        session = self.session
        submissions_resp = check_page_auth(session, ASSIGNMENT_SUBMISSIONS_ENDPOINT)
        submissions_soup = BeautifulSoup(submissions_resp.text, "html.parser")
        # select submissions (class of td.table--primaryLink a tag, submission id stored in href link)
        submissions_a_tags = submissions_soup.select("td.table--primaryLink a")
        submission_ids = [
            a_tag.attrs.get("href").split("/")[-1] for a_tag in submissions_a_tags
        ]
        submission_links = {}
        for submission_id in submission_ids:  # doesn't support image submissions yet
            aws_links = get_submission_files(
                session, course_id, assignment_id, submission_id
            )
            submission_links[submission_id] = aws_links
            # sleep for 0.1 seconds to avoid sending too many requests to gradescope
            time.sleep(0.1)
        return submission_links

    def get_assignment_submissions_for_each_users(
        self, course_id: str, assignment_id: str, get_past_submissions: bool = False
    ):
        ASSIGNMENT_ENDPOINT = f"{self.gradescope_base_url}/courses/{course_id}/assignments/{assignment_id}"
        ASSIGNMENT_SUBMISSIONS_ENDPOINT = f"{ASSIGNMENT_ENDPOINT}/review_grades"
        if not course_id or not assignment_id:
            raise Exception("One or more invalid parameters")
        session = self.session
        submissions_resp = check_page_auth(session, ASSIGNMENT_SUBMISSIONS_ENDPOINT)
        submissions_soup = BeautifulSoup(submissions_resp.text, "html.parser")
        submission_tds = submissions_soup.select("td.table--primaryLink")
        submission_tds_filtered = []
        submit_id_set = set()
        for td in submission_tds:
            tag = td.find("a")
            if tag is not None:
                href = tag.attrs.get("href")
                if href is not None:
                    td_sub_id = href.split("/")[-1]
                    if "," not in tag.text and td_sub_id not in submit_id_set:
                        submit_id_set.add(td_sub_id)
                        submission_tds_filtered.append(td)

        submissions_tds = [
            [td] + td.find_next_siblings("td") for td in submission_tds_filtered
        ]
        submission_infos = [get_user_submission_info(tds) for tds in submissions_tds]
        print_str = ""
        if get_past_submissions:
            for info_i, info in enumerate(submission_infos):
                ASSIGNMENT_ENDPOINT = f"{self.gradescope_base_url}/courses/{course_id}/assignments/{assignment_id}"

                submission_link = f"{ASSIGNMENT_ENDPOINT}/submissions/{info['submissions'][0]['submission_id']}.json?content=react&only_keys%5B%5D=past_submissions"
                submission_histories = json.loads(session.get(submission_link).text)[
                    "past_submissions"
                ]
                active_submission_tz = datetime.fromisoformat(
                    info["submissions"][0]["datetime"]
                ).tzinfo
                for sub_hist_i, sub_hist in enumerate(submission_histories):
                    if len(print_str) > 0:
                        print(" " * len(print_str), end="\r", flush=True)
                    print_str = f"Retrieving download links for user: {info_i + 1}/{len(submission_infos)} sub: {sub_hist_i + 1}/{len(submission_histories)}"
                    print(print_str, end="\r", flush=True)
                    if sub_hist_i == 0:
                        sub_info = info["submissions"][0]
                    else:
                        sub_info = {"submission_id": str(sub_hist["id"])}
                    sub_time = datetime.fromisoformat(
                        sub_hist["created_at"]
                    ).astimezone(active_submission_tz)
                    sub_info["datetime"] = sub_time.isoformat()
                    sub_info["epochtime_s"] = sub_time.timestamp()
                    sub_info["gradescope_submission_link"] = (
                        f"{ASSIGNMENT_ENDPOINT}/submissions/{sub_info['submission_id']}"
                    )

                    if len(sub_hist["owners"]) == 1:
                        sub_info["active"] = sub_hist["owners"][0]["active"]
                    sub_info["links"] = get_submission_files(
                        session, course_id, assignment_id, sub_info["submission_id"]
                    )
                    if sub_hist_i > 0:
                        info["submissions"].append(sub_info)
                    # time.sleep(0.1)
        else:
            for info_i, info in enumerate(submission_infos):
                print(
                    f"Retrieving download links for {info_i + 1}/{len(submission_infos)} user active submission      ",
                    end="\r",
                    flush=True,
                )

                info["submissions"][0]["links"] = get_submission_files(
                    session,
                    course_id,
                    assignment_id,
                    info["submissions"][0]["submission_id"],
                )
                info["submissions"][0]["active"] = True
                # time.sleep(0.1)

        return submission_infos

    def get_assignment_submission(
        self, student_email: str, course_id: str, assignment_id: str
    ) -> list[str]:
        """
        Get a list of aws links to files of the student's most recent submission to an assignment
        Returns:
            list: A list of aws links as strings
            For example:
                [
                    'aws_link1.com',
                    'aws_link2.com',
                    ...
                ]
        Raises:
             Exceptions:
                "One or more invalid parameters": if course_id or assignment_id is null or empty value
                "You are not authorized to access this page.": if logged in user is unable to access submissions
                "You must be logged in to access this page.": if no user is logged in
                "Page not Found": When link is invalid: change in url, invalid course_if or assignment id
                "PDF/Image only submissions not yet supported": assignment is pdf/image submission only, which is not yet supported
                "No submission found": When no submission is found for given student_email
        NOTE: so far only accessible for teachers, not for students to get their own submission
        """
        # fetch submission id
        ASSIGNMENT_ENDPOINT = f"{self.gradescope_base_url}/courses/{course_id}/assignments/{assignment_id}"
        ASSIGNMENT_SUBMISSIONS_ENDPOINT = f"{ASSIGNMENT_ENDPOINT}/review_grades"
        if not (student_email and course_id and assignment_id):
            raise Exception("One or more invalid parameters")
        session = self.session
        submissions_resp = check_page_auth(session, ASSIGNMENT_SUBMISSIONS_ENDPOINT)
        submissions_soup = BeautifulSoup(submissions_resp.text, "html.parser")
        td_with_email = submissions_soup.find(
            "td", string=lambda s: student_email in str(s)
        )
        if td_with_email:
            # grab submission from previous td
            submission_td = td_with_email.find_previous_sibling()
            # submission_td will have an anchor element as a child if there is a submission
            a_element = submission_td.find("a")
            if a_element:
                submission_id = a_element.get("href").split("/")[-1]
            else:
                raise Exception("No submission found")
            # call get_submission_files helper function
            aws_links = get_submission_files(
                session, course_id, assignment_id, submission_id
            )
            return aws_links
        else:
            raise Exception("No submission found")

    def get_assignment_graders(self, course_id: str, question_id: str) -> set[str]:
        """
        Get a set of graders for a specific question in an assignment
        Returns:
            set: A set of graders as strings
            For example:
                {
                    'grader1',
                    'grader2',
                    ...
                }
        Raises:
            Exceptions:
                "One or more invalid parameters": if course_id or assignment_id is null or empty value
                "You are not authorized to access this page.": if logged in user is unable to access submissions
                "You must be logged in to access this page.": if no user is logged in
                "Page not Found": When link is invalid: change in url, invalid course_if or assignment id
        """
        QUESTION_ENDPOINT = (
            f"{self.gradescope_base_url}/courses/{course_id}/questions/{question_id}"
        )
        ASSIGNMENT_SUBMISSIONS_ENDPOINT = f"{QUESTION_ENDPOINT}/submissions"
        if not course_id or not question_id:
            raise Exception("One or more invalid parameters")
        session = self.session
        submissions_resp = check_page_auth(session, ASSIGNMENT_SUBMISSIONS_ENDPOINT)
        submissions_soup = BeautifulSoup(submissions_resp.text, "html.parser")
        # select graders (class of td tag, grader name stored in text)
        graders = submissions_soup.select("td")[2::3]
        grader_names = set(
            [grader.text for grader in graders if grader.text]
        )  # get non-empty grader names
        return grader_names
