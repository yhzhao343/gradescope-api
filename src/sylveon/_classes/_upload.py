"""Functions for uploading assignments to Gradescope.
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from requests_toolbelt.multipart.encoder import MultipartEncoder
import mimetypes
import io
import pathlib


def upload_assignment(
    session: requests.Session,
    course_id: str,
    assignment_id: str,
    *files: io.TextIOWrapper,
):
    """
    Upload an assignment to Gradescope.
    """
    GS_COURSE_ENDPOINT = f"https://www.gradescope.com/courses/{course_id}"
    GS_UPLOAD_ENDPOINT = f"https://www.gradescope.com/courses/{course_id}/assignments/{assignment_id}/submissions"

    # Get auth token
    response = session.get(GS_COURSE_ENDPOINT)
    soup = BeautifulSoup(response.text, "html.parser")
    auth_token = soup.find("meta", {"name": "csrf-token"})["content"]

    form_files = []
    for file in files:
        form_files.append(
            (
                "submission[files][]",
                (
                    pathlib.Path(file.name).name,
                    file,
                    mimetypes.guess_type(file.name)[0],
                ),
            )
        )

    # Setup multipart form data
    multipart = MultipartEncoder(
        fields=(
            ("utf8", "✓"),
            ("authenticity_token", auth_token),
            ("submission[method]", "upload"),
            ("submission[leaderboard_name]", "test"),
            *form_files,
        )
    )

    headers = {
        "Content-Type": multipart.content_type,
        "Referer": GS_COURSE_ENDPOINT,
    }
    response = session.post(GS_UPLOAD_ENDPOINT, data=multipart, headers=headers)

    return response.status_code == 200
