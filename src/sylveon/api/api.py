from fastapi import FastAPI
from sylveon._config.config import (
    SessionModel,
    ConnectionModel,
    TokenModel,
    CourseModel,
    UserModel,
    AssignmentModel,
    SubmissionModel,
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/login")
def login(username: str, password: str):
    """_summary_

    Args:
        username (str): _description_
        password (str): _description_

    Returns:
        TokenModel: _description_
    """
    pass


@app.get("/account")
def get_courses(token: TokenModel):
    """_summary_

    Args:
        token (TokenModel): _description_

    Returns:
        CourseModel: _description_
    """
    pass


@app.get("/courses/{course_id}/memberships")
def get_course_memberships(token: TokenModel, course_id: str):
    """_summary_

    Args:
        token (TokenModel): _description_
        course_id (str): _description_

    Returns:
        UserModel: _description_
    """
    pass


@app.get("/courses/{course_id}")
def get_assignments(token: TokenModel, course_id: str):
    """_summary_

    Args:
        token (TokenModel): _description_
        course_id (str): _description_

    Returns:
        AssignmentModel: _description_
    """
    pass


@app.get("/courses/{course_id}/assignments/{assignment_id}/submissions/{submission_id}")
def get_assignment_submission(
    token: TokenModel, course_id: str, assignment_id: str, submission_id: str
):
    """_summary_

    Args:
        token (TokenModel): _description_
        assignment_id (str): _description_

    Returns:
        SessionModel: _description_
    """
    pass


def update_assignment_due_date(
    token: TokenModel, course_id: str, assignment_id: str, new_due_date: str
) -> bool:
    """_summary_

    Args:
        token (TokenModel): _description_
        assignment_id (str): _description_

    Returns:
        bool: if updating the assignment release date was successful, returns True
              otherwise returns False
    """
    return False


def update_assignment_late_due_date(
    token: TokenModel, course_id: str, assignment_id: str, new_late_due_date: str
) -> bool:
    """_summary_

    Args:
        token (TokenModel): _description_
        assignment_id (str): _description_

    Returns:
        bool: if updating the assignment release date was successful, returns True
              otherwise returns False
    """
    return False


def update_assignment_release_date(
    token: TokenModel, course_id: str, assignment_id: str, new_release_date: str
) -> bool:
    """_summary_

    Args:
        token (TokenModel): _description_
        assignment_id (str): _description_

    Returns:
        bool: if updating the assignment release date was successful, returns True
              otherwise returns False
    """
    return False


def get_extensions(token: TokenModel, course_id: str, assignment_id: str):
    """_summary_

    Args:
        token (TokenModel): _description_
        assignment_id (str): _description_

    Returns:
        __type__: _description_
    """
    pass


def update_student_due_date(
    token: TokenModel, student_id: str, course_id: str, assignment_id: str
) -> bool:
    """_summary_

    Args:
        token (TokenModel): _description_
        student_id (str): _description_
        assignment_id (str): _description_

    Returns:
        bool: if updating the student due date was successful, returns True
              otherwise returns False
    """
    return False


def update_student_late_due_date(
    token: TokenModel, student_id: str, course_id: str, assignment_id: str
) -> bool:
    """_summary_

    Args:
        token (TokenModel): _description_
        student_id (str): _description_
        assignment_id (str): _description_

    Returns:
        bool: if updating the student late due date was successful, returns True
              otherwise returns False
    """
    return False


def update_student_release_date(
    token: TokenModel, student_id: str, course_id: str, assignment_id: str
) -> bool:
    """_summary_

    Args:
        token (TokenModel): _description_
        student_id (str): _description_
        assignment_id (str): _description_

    Returns:
        bool: if updating the student release date was successful, returns True
              otherwise returns False
    """
    return False
