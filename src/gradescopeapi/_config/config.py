"""config.py
Configuration file for FastAPI. Specifies the specific objects and data models used in our api
"""

from datetime import datetime
from typing import Optional
import requests
from enum import Enum
from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    email: str
    password: str


class CourseID(BaseModel):
    course_id: str


class AssignmentID(BaseModel):
    course_id: str
    assignment_id: str


class AssignmentDates(BaseModel):
    course_id: str
    assignment_id: str
    release_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    late_due_date: Optional[datetime] = None


class StudentSubmission(BaseModel):
    student_email: str
    course_id: str
    assignment_id: str


class ExtensionData(BaseModel):
    course_id: str
    assignment_id: str


class UpdateExtensionData(BaseModel):
    course_id: str
    assignment_id: str
    user_id: str
    release_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    late_due_date: Optional[datetime] = None


class AssignmentUpload(BaseModel):
    course_id: str
    assignment_id: str
    leaderboard_name: str | None = None
