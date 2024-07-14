from enum import Enum

from pydantic import BaseModel


class RoleDto(Enum):
    PRACTITIONER = "practitioner"
    PATIENT = "patient"
    ALL = "all"


class RegisterUserDto(BaseModel):
    email: str
    password: str
    role: RoleDto


class LoginUserDto(BaseModel):
    email: str
    password: str
