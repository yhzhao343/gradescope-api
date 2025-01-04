import os

import pytest
from dotenv import load_dotenv

from gradescopeapi.classes.assignments import Assignment
from gradescopeapi.classes.connection import GSConnection

# Load .env file
load_dotenv()
GRADESCOPE_CI_INSTRUCTOR_EMAIL = os.getenv("GRADESCOPE_CI_INSTRUCTOR_EMAIL")
GRADESCOPE_CI_INSTRUCTOR_PASSWORD = os.getenv("GRADESCOPE_CI_INSTRUCTOR_PASSWORD")
GRADESCOPE_CI_STUDENT_EMAIL = os.getenv("GRADESCOPE_CI_STUDENT_EMAIL")


def get_account(account_type="instructor"):
    """Creates a connection and returns the account for testing"""
    connection = GSConnection()
    if account_type == "instructor":
        connection.login(
            GRADESCOPE_CI_INSTRUCTOR_EMAIL, GRADESCOPE_CI_INSTRUCTOR_PASSWORD
        )
    else:
        raise ValueError("Invalid account type: must be 'instructor'")
    return connection.account


def test_get_assignments():
    """Test fetching assignments with valid course ID."""
    account = get_account("instructor")
    course_id = "753413"
    assignments = account.get_assignments(course_id)
    assert isinstance(assignments, list), "Should return a list of assignments"
    assert len(assignments) > 0, "Should contain at least 1 assignment"
    assert all(
        isinstance(a, Assignment) for a in assignments
    ), "All items should be Assignment instances"


def test_get_assignment_submissions():
    """Test fetching assignment submissions with valid course and assignment IDs."""
    account = get_account("instructor")
    course_id = "753413"
    assignment_id = "4330410"

    submissions = account.get_assignment_submissions(course_id, assignment_id)
    assert isinstance(submissions, dict), "Should return a dictionary of submissions"
    assert len(submissions) > 0, "Should contain at least 1 submission"
    assert all(
        isinstance(links, list) for links in submissions.values()
    ), "Each submission ID should map to a list of links"


def test_get_assignment_submission_valid():
    """Test fetching a specific assignment submission."""
    account = get_account("instructor")
    student_email = GRADESCOPE_CI_STUDENT_EMAIL
    course_id = "753413"
    assignment_id = "4330410"
    expected_num_files = 3

    submission = account.get_assignment_submission(
        student_email, course_id, assignment_id
    )
    assert isinstance(submission, list), "Should return a list of aws links"
    assert len(submission) == expected_num_files, "List should contain aws links"


def test_get_assignment_submission_no_submission_found():
    """Test case when no submission is found for a given student."""
    account = get_account("instructor")
    student_email = GRADESCOPE_CI_INSTRUCTOR_EMAIL
    course_id = "753413"
    assignment_id = "5525291"

    with pytest.raises(Exception, match="No submission found"):
        account.get_assignment_submission(student_email, course_id, assignment_id)
