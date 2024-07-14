from typing import Set, List
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Float, Column, Enum, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from .enums import KYCStatus, AppointmentStatus, Role


class Base(DeclarativeBase):
    pass


practitioner_service = Table(
    "association_table",
    Base.metadata,
    Column("practitioner_id", ForeignKey("practitioner_table.id"), primary_key=True),
    Column("service_id", ForeignKey("service_table.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password:  Mapped[str] = mapped_column(String(200))
    role = Column(Enum(Role), nullable=False)

    patient = relationship("Patient", back_populates="user", uselist=False, cascade="all, delete-orphan")
    practitioner = relationship("Practitioner", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Patient(Base):
    __tablename__ = "patient_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), name="firstname")
    last_name: Mapped[str] = mapped_column(String(30), name="lastname")
    age: Mapped[int] = mapped_column(Integer(), nullable=True)

    user_id : Mapped["User"] = mapped_column(Integer(), ForeignKey("user_table.id"))
    user = relationship("User",back_populates="patient", uselist=False)

    patient_profile_picture : Mapped["PatientProfilePicture"] = relationship(
        back_populates="patient", cascade="all, delete-orphan",
        uselist=False
    )
    patient_location : Mapped["PatientLocation"] = relationship(
        back_populates="patient", cascade="all, delete-orphan",
        uselist=False
    )
    appointments : Mapped[Set["Appointment"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan",
        uselist=True
    )


class PatientProfilePicture(Base):
    __tablename__ = "patient_profile_picture_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patient_table.id"))
    patient: Mapped["Patient"] = relationship(
        back_populates="patient_profile_picture",
        uselist=False
    )


class PatientLocation(Base):
    __tablename__ = "patient_location_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(80), nullable=False)
    lattitude: Mapped[float] = mapped_column(Float(), nullable=True)
    longitude: Mapped[float] = mapped_column(Float(), nullable=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patient_table.id"))
    patient: Mapped["Patient"] = relationship(
        back_populates="patient_location",
        uselist=False
    )


class Appointment(Base):
    __tablename__ = "appointment_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patient_table.id"))
    patient: Mapped["Patient"] = relationship(
        back_populates="appointments",
        uselist=False
    )
    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="appointments",
        uselist=False
    )
    appointment_state: Mapped["AppointmentState"] = relationship(
        back_populates="appointment",
        uselist=False
    )
    service_id: Mapped[int] = mapped_column(ForeignKey("service_table.id"))
    service: Mapped["Service"] = relationship(
        back_populates="appointments",
        uselist=False
    )

    day_id: Mapped[int] = mapped_column(ForeignKey("day_table.id"))
    day: Mapped["Day"] = relationship(
        back_populates="appointments",
        uselist=False
    )


class AppointmentState(Base):
    __tablename__ = "appointment_state_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.CREATED, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment_table.id"))
    appointment: Mapped["Appointment"] = relationship(
        back_populates="appointment_state",
        uselist=False
    )


class Practitioner(Base):
    __tablename__ = "practitioner_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(30), name="firstname")
    last_name: Mapped[str] = mapped_column(String(30), name="lastname")
    age: Mapped[int] = mapped_column(Integer(), nullable=True)

    user_id : Mapped["User"] = mapped_column(Integer(), ForeignKey("user_table.id"))
    user = relationship("User", back_populates="practitioner", uselist=False)

    kyc: Mapped["Kyc"] = relationship(
        back_populates="practitioner", cascade="all, delete-orphan",
        uselist=False
    )
    location : Mapped["PractitionerLocation"] = relationship(
        back_populates="practitioner", cascade="all, delete-orphan",
        uselist=False
    )

    profile_picture : Mapped["PractitionerProfilePicture"] = relationship(
        back_populates="practitioner", cascade="all, delete-orphan",
        uselist=False
    )
    appointments : Mapped[Set["Appointment"]] = relationship(
        back_populates="practitioner", cascade="all, delete-orphan",
        uselist=True
    )
    services: Mapped[List["Service"]] = relationship(
        secondary=practitioner_service, back_populates="practitioners",
        uselist=True
    )
    days: Mapped[List["Day"]] = relationship(
        back_populates="practitioner",
        uselist=True
    )


class Kyc(Base):
    __tablename__ = "kyc_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    status = Column(Enum(KYCStatus), default=KYCStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="kyc",
        uselist=False
    )


class PractitionerProfilePicture(Base):
    __tablename__ = "practitioner_profile_picture_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="profile_picture",
        uselist=False
    )


class PractitionerLocation(Base):
    __tablename__ = "practitioner_location_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(80), nullable=False)
    lattitude: Mapped[float] = mapped_column(Float(), nullable=True)
    longitude: Mapped[float] = mapped_column(Float(), nullable=True)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="location",
        uselist=False
    )


class Service(Base):
    __tablename__ = "service_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    practitioners: Mapped[List["Practitioner"]] = relationship(
        secondary=practitioner_service, back_populates="services",
        uselist=True
    )
    appointments: Mapped[Set["Appointment"]] = relationship(
        back_populates="service",
        uselist=True
    )



class Day(Base):
    __tablename__ = "day_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    dayOfWeek: Mapped[int] = mapped_column(Integer(), nullable=False)
    weekNumber: Mapped[int] = mapped_column(Integer(), nullable=False)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="days",
        uselist=False
    )
    appointments: Mapped[Set["Appointment"]] = relationship(
        back_populates="day",
        uselist=True
    )

  