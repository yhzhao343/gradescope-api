import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import datetime

"""
Functions for getting, adding, and changing student extensions on assignments.
get_extensions()
update_student_due_date()
update_student_late_due_date()
update_student_release_date()
"""


@dataclass
class Extension:
    # user_id: str
    release_date: datetime.datetime
    due_date: datetime.datetime
    late_due_date: datetime.datetime


def get_extensions(
    session: requests.Session, course_id: str, assignment_id: str
) -> dict:
    """
    Get all extensions for an assignment.
    {
        user_id: Extension,
        user_id: Extension,
        ...
    }
    """
    GS_EXTENSIONS_ENDPOINT = f"https://www.gradescope.com/courses/{course_id}/assignments/{assignment_id}/extensions"
    GS_EXTENSIONS_TABLE_CSS_ID = "DataTables_Table_0"

    # get the extensions from the page
    response = session.get(GS_EXTENSIONS_ENDPOINT)

    # check if the request was successful
    if response.status_code != 200:
        raise Exception(
            f"Failed to get extensions for assignment {assignment_id}. Status code: {response.status_code}"
        )

    # parse the html response
    extensions_soup = BeautifulSoup(response.text, "html.parser")

    extensions_table = extensions_soup.find("table", id=GS_EXTENSIONS_TABLE_CSS_ID)
    extensions_table = extensions_soup.find(
        "table", attrs={"id": GS_EXTENSIONS_TABLE_CSS_ID}
    )

    extensions = {}

    # return the extensions
    return extensions


def update_student_extension(
    session: requests.Session,
    course_id: str,
    assignment_id: str,
    user_id: str,
    release_date: datetime.datetime | None = None,
    due_date: datetime.datetime | None = None,
    late_due_date: datetime.datetime | None= None,
) -> bool:
    """Updates the extension for a student on an assignment

    If the user currently has an extension, this will overwrite their
    current extension. If the user does not have an extension, this
    will add an extension for that user. If a date is None, it will
    not be updated.

    Requirements:
        release_date <= due_date <= late_due_date
    
    Notes:
        Extensions can go "backwards" too. For example, a user can have
        a release date earlier than the normal release date or a due date
        before the normal due date.

    Args:
        session: The session to use for the request
        course_id: The course id
        assignment_id: The assignment id
        user_id: The user id
        release_date: The release date. If None, it will not be updated
        due_date: The due date. If None, it will not be updated
        late_due_date: The late due date. If None, it will not be updated
    """

    # Check if at least 1 date is set
    if release_date is None and due_date is None and late_due_date is None:
        raise ValueError("At least one date must be provided")

    # Check if date requirements are met (in order)
    dates = [date for date in [release_date, due_date, late_due_date] if date is not None]
    if dates != sorted(dates):
        raise ValueError("Dates must be in order: release_date <= due_date <= late_due_date")

    def add_to_body(extension_name: str, extension_datetime: datetime.datetime):
        """Update JSON body for POST request"""
        if extension_datetime is not None:
            # convert datetime to UTC
            extension_datetime = extension_datetime.astimezone(datetime.timezone.utc)

            # convert datetime to string ISO 8601 format
            date_str = extension_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

            # add to request body
            body["override"]["settings"][extension_name] = {
                "type": "absolute",
                "value": date_str,
            }

    # Update release date, due date, and late due date
    body = {"override": {"user_id": user_id, "settings": {}}}
    for extension_name, extension_datetime in [
        ("release_date", release_date),
        ("due_date", due_date),
        ("hard_due_date", late_due_date),
    ]:
        if extension_datetime is not None:
            add_to_body(extension_name, extension_datetime)

    # send the request
    resp = session.post(
        f"https://www.gradescope.com/courses/{course_id}/assignments/{assignment_id}/extensions",
        json=body,
    )
    return resp.status_code == 200


def remove_student_extension():
    pass
