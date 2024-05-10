from dataclasses import dataclass


@dataclass
class Member:
    full_name: str
    email: str
    role: str
    id: str
    num_submissions: int
