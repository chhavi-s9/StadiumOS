"""
=========================================================
stadium.py

Physical stadium infrastructure models.

Responsibilities
----------------
- Zones
- Gates
- Food Courts
- Washrooms
- Parking Areas

=========================================================
"""

from __future__ import annotations

from pydantic import Field

from .base import (
    CrowdLevel,
    GateStatus,
    Position,
    StadiumBaseModel,
    ZoneStatus,
)


# =========================================================
# Zone
# =========================================================

class Zone(StadiumBaseModel):
    """
    Represents a stadium zone.
    """

    id: str
    name: str

    position: Position

    capacity: int

    current_occupancy: int = 0

    crowd_level: CrowdLevel = CrowdLevel.LOW

    status: ZoneStatus = ZoneStatus.OPEN

    connected_gates: list[str] = Field(default_factory=list)


# =========================================================
# Gate
# =========================================================

class Gate(StadiumBaseModel):
    """
    Entry / Exit gate.
    """

    id: str

    name: str

    serves_zone: str

    position: Position

    capacity_per_minute: int

    current_queue: int = 0

    status: GateStatus = GateStatus.OPEN


# =========================================================
# Food Court
# =========================================================

class FoodCourt(StadiumBaseModel):
    """
    Food court inside the stadium.
    """

    id: str

    name: str

    zone_id: str

    position: Position

    vendors: int = 5

    average_wait_minutes: int = 0


# =========================================================
# Washroom
# =========================================================

class Washroom(StadiumBaseModel):
    """
    Washroom facility.
    """

    id: str

    zone_id: str

    position: Position

    capacity: int

    occupied: int = 0


# =========================================================
# Parking Area
# =========================================================

class ParkingArea(StadiumBaseModel):
    """
    Stadium parking area.
    """

    id: str

    name: str

    position: Position

    capacity: int

    occupied_spaces: int = 0