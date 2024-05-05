import requests
import os
from dotenv import load_dotenv
import pytest
from datetime import datetime, timedelta

from sylveon._classes._connection import GSConnection

from sylveon._classes._upload import upload_assignment

# load .env file
load_dotenv()

GRADESCOPE_CI_STUDENT_EMAIL = os.getenv("GRADESCOPE_CI_STUDENT_EMAIL")
GRADESCOPE_CI_STUDENT_PASSWORD = os.getenv("GRADESCOPE_CI_STUDENT_PASSWORD")
GRADESCOPE_CI_INSTRUCTOR_EMAIL = os.getenv("GRADESCOPE_CI_INSTRUCTOR_EMAIL")
GRADESCOPE_CI_INSTRUCTOR_PASSWORD = os.getenv("GRADESCOPE_CI_INSTRUCTOR_PASSWORD")


def new_session(account_type="student"):
    """Creates and returns a session for testing"""
    connection = GSConnection()

    match account_type.lower():
        case "student":
            connection.login(
                GRADESCOPE_CI_STUDENT_EMAIL, GRADESCOPE_CI_STUDENT_PASSWORD
            )
        case "instructor":
            connection.login(
                GRADESCOPE_CI_INSTRUCTOR_EMAIL, GRADESCOPE_CI_INSTRUCTOR_PASSWORD
            )
        case _:
            raise ValueError("Invalid account type: must be 'student' or 'instructor'")

    return connection.session


def test_upload():
    # create test session
    test_session = new_session("student")

    course_id = "753413"
    assignment_id = "4330410"

    with (
        open("tests/upload_files/text_file.txt", "rb") as text_file,
        open("tests/upload_files/markdown_file.md", "rb") as markdown_file,
        open("tests/upload_files/python_file.py", "rb") as python_file,
    ):

        extensions = upload_assignment(
            test_session,
            course_id,
            assignment_id,
            text_file,
            markdown_file,
            python_file,
        )

    assert extensions
