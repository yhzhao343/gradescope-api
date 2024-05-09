import os
from dotenv import load_dotenv

from gradescopeapi._classes._connection import GSConnection

# load .env file
load_dotenv()
GRADESCOPE_CI_STUDENT_EMAIL = os.getenv("GRADESCOPE_CI_STUDENT_EMAIL")
GRADESCOPE_CI_STUDENT_PASSWORD = os.getenv("GRADESCOPE_CI_STUDENT_PASSWORD")
GRADESCOPE_CI_INSTRUCTOR_EMAIL = os.getenv("GRADESCOPE_CI_INSTRUCTOR_EMAIL")
GRADESCOPE_CI_INSTRUCTOR_PASSWORD = os.getenv("GRADESCOPE_CI_INSTRUCTOR_PASSWORD")

# TODO:
# - Test for exact course info
# - Test for users that are both instructors and students


def test_get_courses_student():
    # create connection object
    conn_student = GSConnection()

    # login and fetch account
    conn_student.login(GRADESCOPE_CI_STUDENT_EMAIL, GRADESCOPE_CI_STUDENT_PASSWORD)
    account = conn_student.account

    # get courses
    courses = account.get_courses()

    assert courses["instructor"] == {} and courses["student"] != {}


def test_get_courses_instructor():
    # create connection object
    conn_instr = GSConnection()

    # login and fetch account
    conn_instr.login(GRADESCOPE_CI_INSTRUCTOR_EMAIL, GRADESCOPE_CI_INSTRUCTOR_PASSWORD)
    account = conn_instr.account

    # get courses
    courses = account.get_courses()

    assert courses["instructor"] != {} and courses["student"] == {}
