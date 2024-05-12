import io
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from typing import Dict, List
import requests
import os
import io
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from typing import Dict, List
import requests
import os
from gradescopeapi._config.config import (
    AssignmentUpload,
    ExtensionData,
    LoginRequestModel,
    CourseID,
    AssignmentID,
    StudentSubmission,
    AssignmentDates,
    UpdateExtensionData
)
from gradescopeapi.classes.account import Account
from gradescopeapi.classes.assignments import Assignment, update_assignment_date
from gradescopeapi.classes.connection import GSConnection
from gradescopeapi.classes.extensions import get_extensions, update_student_extension
from gradescopeapi.classes.upload import upload_assignment

app = FastAPI()

# Create instance of GSConnection, to be used where needed
connection = GSConnection()


def get_gs_connection():
    """
    Returns the GSConnection instance

    Returns:
        connection (GSConnection): an instance of the GSConnection class,
            containing the session object used to make HTTP requests,
            a boolean defining True/False if the user is logged in, and
            the user's Account object.
    """
    return connection


def get_gs_connection_session():
    """
    Returns session of the the GSConnection instance

    Returns:
        connection.session (GSConnection.session): an instance of the GSConnection class' session object used to make HTTP requests
    """
    return connection.session


def get_account():
    """
    Returns the user's Account object

    Returns:
        Account (Account): an instance of the Account class, containing
            methods for interacting with the user's courses and assignments.
    """
    return Account(session=get_gs_connection_session)

# Create instance of GSConnection, to be used where needed
connection = GSConnection()


def get_gs_connection():
    """
    Returns the GSConnection instance

    Returns:
        connection (GSConnection): an instance of the GSConnection class,
            containing the session object used to make HTTP requests,
            a boolean defining True/False if the user is logged in, and
            the user's Account object.
    """
    return connection


def get_gs_connection_session():
    """
    Returns session of the the GSConnection instance

    Returns:
        connection.session (GSConnection.session): an instance of the GSConnection class' session object used to make HTTP requests
    """
    return connection.session


def get_account():
    """
    Returns the user's Account object

    Returns:
        Account (Account): an instance of the Account class, containing
            methods for interacting with the user's courses and assignments.
    """
    return Account(session=get_gs_connection_session)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/login", name="login")
def login(
    login_data: LoginRequestModel,
    gs_connection: GSConnection = Depends(get_gs_connection),
):
    """Login to Gradescope, with correct credentials
@app.post("/login", name="login")
def login(
    login_data: LoginRequestModel,
    gs_connection: GSConnection = Depends(get_gs_connection),
):
    """Login to Gradescope, with correct credentials

    Args:
        username (str): email address of user attempting to log in
        password (str): password of user attempting to log in

    Raises:
        HTTPException: If the request to login fails, with a 404 Unauthorized Error status code and the error message "Account not found".
    """
    user_email = login_data.email
    password = login_data.password

    try:
        connection.login(user_email, password)
        return {"message": "Login successful", "status_code": status.HTTP_200_OK}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Account not found. Error {e}")


@app.post("/courses", response_model=Dict[str, Dict[str, Dict]])
def get_courses(account: Account = Depends(get_account)):
    """Get all courses for the user

    Args:
        account (Account): Account object containing the user's courses
        account (Account): Account object containing the user's courses

    Returns:
        dict: dictionary of dictionaries

    Raises:
        HTTPException: If the request to get courses fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        course_list = account.get_courses()
        return course_list
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/course_users", response_model=List[str])
def get_course_users(course_id: str, account: Account = Depends(get_account)):
    """Get all users for a course
        dict: dictionary of dictionaries

    Raises:
        HTTPException: If the request to get courses fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        course_list = account.get_courses()
        return course_list
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/course_users", response_model=List[str])
def get_course_users(course_id: str, account: Account = Depends(get_account)):
    """Get all users for a course

    Args:
        course_id (str): ID of the course
        course_id (str): ID of the course

    Returns:
        list: list of user emails

    Raises:
        HTTPException: If the request to get course users fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        course_users = account.get_course_users(course_id)
        return course_users
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get course users. Error {e}"
        )


@app.post("/assignments", response_model=List[Assignment])
def get_assignments(course_id: CourseID, account: Account = Depends(get_account)):
    """Get all assignments for a course
        list: list of user emails

    Raises:
        HTTPException: If the request to get course users fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        course_users = account.get_course_users(course_id)
        return course_users
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get course users. Error {e}"
        )


@app.post("/assignments", response_model=List[Assignment])
def get_assignments(course_id: CourseID, account: Account = Depends(get_account)):
    """Get all assignments for a course

    Args:
        course_id (str): ID of the course
        course_id (str): ID of the course

    Returns:
        list: list of Assignment objects

    Raises:
        HTTPException: If the request to get assignments fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        assignment_list = account.get_assignments(course_id.course_id)
        return assignment_list
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get assignments. Error: {e}"
        )


@app.post("/assignment_submissions", response_model=Dict[str, List[str]])
def get_assignment_submissions(
    assignment_id: AssignmentID, account: Account = Depends(get_account)
):
    """Get all assignment submissions for an assignment
        list: list of Assignment objects

    Raises:
        HTTPException: If the request to get assignments fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        assignment_list = account.get_assignments(course_id.course_id)
        return assignment_list
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get assignments. Error: {e}"
        )


@app.post("/assignment_submissions", response_model=Dict[str, List[str]])
def get_assignment_submissions(
    assignment_id: AssignmentID, account: Account = Depends(get_account)
):
    """Get all assignment submissions for an assignment

    Args:
        assignment_id (AssignmentID): ID of the assignment
        assignment_id (AssignmentID): ID of the assignment

    Returns:
        dict: dictionary containing a list of student emails and their corresponding submission IDs

    Raises:
        HTTPException: If the request to get assignment submissions fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        assignment_submissions = account.get_assignment_submissions(
            assignment_id.course_id, assignment_id.assignment_id
        )
        return assignment_submissions
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get assignment submissions. Error: {e}"
        )


@app.post("/assignment_submission", response_model=List[str])
def get_student_assignment_submission(
    student_submission: StudentSubmission, account: Account = Depends(get_account)
):
    """Get a student's assignment submission. ONLY FOR INSTRUCTORS.
        dict: dictionary containing a list of student emails and their corresponding submission IDs

    Raises:
        HTTPException: If the request to get assignment submissions fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        assignment_submissions = account.get_assignment_submissions(
            assignment_id.course_id, assignment_id.assignment_id
        )
        return assignment_submissions
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get assignment submissions. Error: {e}"
        )


@app.post("/assignment_submission", response_model=List[str])
def get_student_assignment_submission(
    student_submission: StudentSubmission, account: Account = Depends(get_account)
):
    """Get a student's assignment submission. ONLY FOR INSTRUCTORS.

    Args:
        student_submission (StudentSubmission): ID of the assignment and student email
        student_submission (StudentSubmission): ID of the assignment and student email

    Returns:
        list: list of file names for the student's submission

    Raises:
        HTTPException: If the request to get assignment submission fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        student_submission = account.get_assignment_submission(
            student_submission.student_email,
            student_submission.course_id,
            student_submission.assignment_id,
        )
        return student_submission
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get assignment submission. Error: {e}"
        )


@app.post("/assignments/update_dates")
def update_assignment_dates(
    assignment_dates: AssignmentDates,
    session: requests.Session = Depends(get_gs_connection_session),
):
    """
    Update the release and due dates for an assignment.

    Args:
        assignment_dates (AssignmentDates): Pydantic model containing the course_id, assignment_id, release_date, due_date, and late_due_date.
        session (requests.Session, optional): The session object used for making HTTP requests.
            Defaults to the session instance provided by the get_session dependency.
        assignment_dates (AssignmentDates): Pydantic model containing the course_id, assignment_id, release_date, due_date, and late_due_date.
        session (requests.Session, optional): The session object used for making HTTP requests.
            Defaults to the session instance provided by the get_session dependency.

    Returns:
        dict: A dictionary with a "message" key indicating if the assignment dates were updated successfully.

    Raises:
        HTTPException: If the assignment dates update fails, with a 400 Bad Request status code and the error message "Failed to update assignment dates".
    """
    try:
        success = update_assignment_date(
            session=session,
            course_id=assignment_dates.course_id,
            assignment_id=assignment_dates.assignment_id,
            release_date=assignment_dates.release_date,
            due_date=assignment_dates.due_date,
            late_due_date=assignment_dates.late_due_date,
        )
        if success:
            return {
                "message": "Assignment dates updated successfully",
                "status_code": status.HTTP_200_OK,
            }
        else:
            raise HTTPException(
                status_code=400, detail="Failed to update assignment dates"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assignments/extensions", response_model=dict)
def get_assignment_extensions(
    extension_data: ExtensionData,
    session: requests.Session = Depends(get_gs_connection_session),
):
    """
    Get all extensions for an assignment.

    Args:
        extension_data (ExtensionData): Pydantic model containing the course_id and assignment_id.
        session (requests.Session, optional): The session object used for making HTTP requests.
            Defaults to the session instance provided by the get_session dependency.

    Returns:
        dict: A dictionary containing the extensions, where the keys are user IDs and the values are Extension objects.

    Raises:
        HTTPException: If the request to get extensions fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        extensions = get_extensions(
            session=session,
            course_id=extension_data.course_id,
            assignment_id=extension_data.assignment_id,
        )
        return extensions
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assignments/extensions/update")
def update_extension(
    update_extension_data: UpdateExtensionData,
    session: requests.Session = Depends(get_gs_connection_session),
):
    """
    Update the extension for a student on an assignment.

    Args:
        update_extension_data (UpdateExtensionData): Pydantic model containing the course_id, assignment_id, user_id,
            and optional release_date, due_date, and late_due_date.
        session (requests.Session, optional): The session object used for making HTTP requests.
            Defaults to the session instance provided by the get_gs_connection_session dependency.

    Returns:
        dict: A dictionary with a "message" key indicating if the extension was updated successfully.

    Raises:
        HTTPException: If the extension update fails, with a 400 Bad Request status code and the error message.
        HTTPException: If a ValueError is raised (e.g., invalid date order), with a 400 Bad Request status code and the error message.
        HTTPException: If any other exception occurs, with a 500 Internal Server Error status code and the error message.
    """
    try:
        success = update_student_extension(
            session=session,
            course_id=update_extension_data.course_id,
            assignment_id=update_extension_data.assignment_id,
            user_id=update_extension_data.user_id,
            release_date=update_extension_data.release_date,
            due_date=update_extension_data.due_date,
            late_due_date=update_extension_data.late_due_date,
        )
        if success:
            return {
                "message": "Extension updated successfully",
                "status_code": status.HTTP_200_OK,
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to update extension")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assignments/upload")
async def upload_assignment_files(
    assignment_upload: AssignmentUpload,
    files: List[UploadFile] = File(...),
    session: requests.Session = Depends(get_gs_connection_session),
):
    """
    Upload files for an assignment.

    Args:
        assignment_upload (AssignmentUpload): Pydantic model containing the course_id, assignment_id, and leaderboard_name.
        files (List[UploadFile]): List of files to be uploaded.
        session (requests.Session, optional): The session object used for making HTTP requests.
            Defaults to the session instance provided by the get_gs_connection_session dependency.
        assignment_upload (AssignmentUpload): Pydantic model containing the course_id, assignment_id, and leaderboard_name.
        files (List[UploadFile]): List of files to be uploaded.
        session (requests.Session, optional): The session object used for making HTTP requests.
            Defaults to the session instance provided by the get_gs_connection_session dependency.

    Returns:
        dict: A dictionary containing the submission link for the uploaded files.

    Raises:
        HTTPException: If the upload fails, with a 400 Bad Request status code and the error message "Upload unsuccessful".
        HTTPException: If any other exception occurs, with a 500 Internal Server Error status code and the error message.
    """
    try:
        file_objects = [io.TextIOWrapper(file.file, encoding="utf-8") for file in files]
        submission_link = upload_assignment(
            session=session,
            course_id=assignment_upload.course_id,
            assignment_id=assignment_upload.assignment_id,
            *file_objects,
            leaderboard_name=assignment_upload.leaderboard_name,
        )
        if submission_link:
            return {"submission_link": submission_link}
        else:
            raise HTTPException(status_code=400, detail="Upload unsuccessful")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        dict: A dictionary containing the submission link for the uploaded files.

    Raises:
        HTTPException: If the upload fails, with a 400 Bad Request status code and the error message "Upload unsuccessful".
        HTTPException: If any other exception occurs, with a 500 Internal Server Error status code and the error message.
    """
    try:
        file_objects = [io.TextIOWrapper(file.file, encoding="utf-8") for file in files]
        submission_link = upload_assignment(
            session=session,
            course_id=assignment_upload.course_id,
            assignment_id=assignment_upload.assignment_id,
            *file_objects,
            leaderboard_name=assignment_upload.leaderboard_name,
        )
        if submission_link:
            return {"submission_link": submission_link}
        else:
            raise HTTPException(status_code=400, detail="Upload unsuccessful")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
