from enum import Enum


class KYCStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AppointmentStatus(Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class WeekNumber(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    LAST = 4


class Role(Enum):
    PRACTITIONER= "practitioner"
    PATIENT ="patient"
    ALL ="all"