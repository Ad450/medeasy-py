from typing import Set, List
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Float, Column, Enum, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Domain.enums import KYCStatus, AppointmentStatus


class Base(DeclarativeBase):
    pass


practitioner_service = Table(
    "association_table",
    Base.metadata,
    Column("practitioner_id", ForeignKey("practitioner_table.id"), primary_key=True),
    Column("service_id", ForeignKey("service_table.id"), primary_key=True),
)


class Patient(Base):
    __table__ = "patient_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), name="firstname")
    last_name: Mapped[str] = mapped_column(String(30), name="lastname")
    age: Mapped[int] = mapped_column(Integer(), nullable=True)
    patient_profile_picture = Mapped["PatientProfilePicture"] = relationship(
        back_populates="patient", cascade="all delete-orphan",
        useList=False
    )
    patient_location = Mapped["PatientLocation"] = relationship(
        back_populates="patient", cascade="all delete-orphan",
        useList=False
    )
    appointments = Mapped[Set["Appointment"]] = relationship(
        back_populates="patient", cascade="all delete-orphan",
        useList=True
    )


class PatientProfilePicture(Base):
    __table__ = "patient_profile_picture_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patient_table.id"))
    patient: Mapped["Patient"] = relationship(
        back_populates="patient_profile_picture",
        useList=False
    )


class PatientLocation(Base):
    __table__ = "patient_location_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(80), nullable=False)
    lattitude: Mapped[float] = mapped_column(Float(), nullable=True)
    longitude: Mapped[float] = mapped_column(Float(), nullable=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patient_table.id"))
    patient: Mapped["Patient"] = relationship(
        back_populates="patient_location",
        useList=False
    )


class Appointment(Base):
    __table__ = "appointment_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("patient_table.id"))
    patient: Mapped["Patient"] = relationship(
        back_populates="appointments",
        useList=False
    )
    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="appointments",
        useList=False
    )
    appointment_state: Mapped["AppointmentState"] = relationship(
        back_populates="appointments",
        useList=False
    )
    service_id: Mapped[int] = mapped_column(ForeignKey("service_table.id"))
    service: Mapped["Service"] = relationship(
        back_populates="appointments",
        useList=False
    )

    day_id: Mapped[int] = mapped_column(ForeignKey("day_table.id"))
    day: Mapped["Day"] = relationship(
        back_populates="appointments",
        useList=False
    )


class AppointmentState(Base):
    __table__ = "appointment_state_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.CREATED, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment_table.id"))
    appointment: Mapped["Appointment"] = relationship(
        back_populates="appointmentstate",
        useList=False
    )


class Practitioner(Base):
    __table__ = "practitioner_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(30), name="firstname")
    last_name: Mapped[str] = mapped_column(String(30), name="lastname")
    age: Mapped[int] = mapped_column(Integer(), nullable=True)

    kyc: Mapped["Kyc"] = relationship(
        back_populates="practitioner", cascade="all delete-orphan",
        useList=False
    )
    location = Mapped["PractitionerLocation"] = relationship(
        back_populates="practitioner", cascade="all delete-orphan",
        useList=False
    )
    appointments = Mapped[Set["Appointment"]] = relationship(
        back_populates="practitioner", cascade="all delete-orphan",
        useList=True
    )
    services: Mapped[List["Service"]] = relationship(
        secondary=practitioner_service, back_populates="practitioners"
    )
    days: Mapped[List["Day"]] = relationship(
        back_populates="practitioner",
        useList=True
    )


class Kyc(Base):
    __table__ = "kyc_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    status = Column(Enum(KYCStatus), default=KYCStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="kyc",
        useList=False
    )


class PractitionerProfilePicture(Base):
    __table__ = "practitioner_profile_picture_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="practitioner_location",
        useList=False
    )


class PractitionerLocation(Base):
    __table__ = "practitioner_location_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_url: Mapped[str] = mapped_column(String(80), nullable=False)
    lattitude: Mapped[float] = mapped_column(Float(), nullable=True)
    longitude: Mapped[float] = mapped_column(Float(), nullable=True)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="practitioner_location",
        useList=False
    )


class Service(Base):
    __table__ = "service_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    practitioners: Mapped[List["Practitioner"]] = relationship(
        secondary=practitioner_service, back_populates="services"
    )
    practitioner: Mapped[Set["Appointment"]] = relationship(
        back_populates="service",
        useList=True
    )


class Day(Base):
    __table__ = "day_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    dayOfWeek: Mapped[int] = mapped_column(Integer(), nullable=False)
    weekNumber: Mapped[int] = mapped_column(Integer(), nullable=False)

    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioner_table.id"))
    practitioner: Mapped["Practitioner"] = relationship(
        back_populates="days",
        useList=False
    )
    appointments: Mapped[Set["Appointment"]] = relationship(
        back_populates="day",
        useList=True
    )

  