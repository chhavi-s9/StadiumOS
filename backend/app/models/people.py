"""
=========================================================
people.py

People models used throughout StadiumOS AI.

Responsibilities
----------------
- Fans
- Volunteers
- Security Officers
- Medical Staff

=========================================================
"""

from __future__ import annotations

from .base import (
    Position,
    StaffRole,
    StadiumBaseModel,
    TaskStatus,
)


# =========================================================
# Fan
# =========================================================

class Fan(StadiumBaseModel):
    """
    Represents a fan inside or around the stadium.
    """

    id: str

    ticket_id: str

    current_zone: str

    destination_zone: str

    position: Position

    is_moving: bool = True

    needs_accessibility: bool = False

    group_size: int = 1


# =========================================================
# Volunteer
# =========================================================

class Volunteer(StadiumBaseModel):
    """
    Volunteer available for stadium assistance.
    """

    id: str

    name: str

    current_zone: str

    position: Position

    role: StaffRole = StaffRole.VOLUNTEER

    current_task: str | None = None

    task_status: TaskStatus = TaskStatus.PENDING

    available: bool = True


# =========================================================
# Security Officer
# =========================================================

class SecurityOfficer(StadiumBaseModel):
    """
    Security personnel deployed across the stadium.
    """

    id: str

    name: str

    current_zone: str

    position: Position

    role: StaffRole = StaffRole.SECURITY

    available: bool = True


# =========================================================
# Medical Staff
# =========================================================

class MedicalStaff(StadiumBaseModel):
    """
    Medical response personnel.
    """

    id: str

    name: str

    current_zone: str

    position: Position

    role: StaffRole = StaffRole.MEDICAL

    available: bool = True