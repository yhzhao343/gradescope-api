from datetime import datetime, timedelta

from gradescopeapi._classes._assignments import update_assignment_date


def test_valid_change_assignment(create_session):
    """Test valid extension for a student."""
    # create test session
    test_session = create_session("instructor")

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
