"""config.py
Configuration file for FastAPI. Specifies the specific objects and data models used in our api
"""

import requests
from enum import Enum
from pydantic import BaseModel


class SemesterModel(str, Enum):
    spring = "spring"
    summer = "summer"
    fall = "fall"
    winter = "winter"


class SessionModel(BaseModel):
    session: requests.Session


class ConnectionModel(BaseModel):
    session: SessionModel
    logged_in: bool = False


class TokenModel(BaseModel):
    access_token: str


class CourseModel(BaseModel):
    course_id: str
    course_short_name: str
    course_name: str
    course_semester: SemesterModel
    course_year: int


class UserModel(BaseModel):
    user_id: str
    user_name: str
    user_email: str


class AssignmentStatusModel(str, Enum):
    submitted = "submitted"
    not_submitted = "not submitted"
    graded = "graded"


class AssignmentModel(BaseModel):
    assignment_id: str
    assignment_name: str
    assignment_release_date: str
    assignment_due_date: str
    assignment_late_due_date: str
    assignment_status: AssignmentStatusModel
    grade: int
    max_grade: int


class SubmissionModel(BaseModel):
    submission_id: str
    submission_link: str
