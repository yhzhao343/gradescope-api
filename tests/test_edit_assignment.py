import requests
import os
from dotenv import load_dotenv
import pytest
from datetime import datetime, timedelta

from sylveon._classes._login_helpers import (
    login_set_session_cookies,
    get_auth_token_init_gradescope_session,
)

from sylveon._classes._connection import GSConnection

from sylveon._classes._assignments import update_assignment_date

# load .env file
load_dotenv()

GRADESCOPE_CI_STUDENT_EMAIL = os.getenv("GRADESCOPE_CI_STUDENT_EMAIL")
GRADESCOPE_CI_STUDENT_PASSWORD = os.getenv("GRADESCOPE_CI_STUDENT_PASSWORD")
GRADESCOPE_CI_INSTRUCTOR_EMAIL = os.getenv("GRADESCOPE_CI_INSTRUCTOR_EMAIL")
GRADESCOPE_CI_INSTRUCTOR_PASSWORD = os.getenv("GRADESCOPE_CI_INSTRUCTOR_PASSWORD")


def test_valid_change_assignment():
    """Test valid extension for a student."""
    # create test session
    test_session = requests.Session()

    # assuming test_get_auth_token_init_gradescope_session works
    auth_token = get_auth_token_init_gradescope_session(test_session)
    login_check = login_set_session_cookies(
        test_session,
        GRADESCOPE_CI_INSTRUCTOR_EMAIL,
        GRADESCOPE_CI_INSTRUCTOR_PASSWORD,
        auth_token,
    )

    course_id = "753413"
    assignment_id = "4436170"
    release_date = datetime(2024, 4, 15)
    due_date = release_date + timedelta(days=1)
    late_due_date = due_date + timedelta(days=1)

    result = update_assignment_date(
        test_session,
        course_id,
        assignment_id,
        release_date,
        due_date,
        late_due_date,
    )
    assert result
