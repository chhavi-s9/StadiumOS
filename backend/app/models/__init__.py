"""
Models package for StadiumOS AI.

This package exposes all domain models through a single
import point.
"""

# Shared Types
from .base import (
    AgentType,
    AlertLevel,
    CrowdLevel,
    GateStatus,
    IncidentSeverity,
    IncidentType,
    Position,
    RouteType,
    StadiumBaseModel,
    StaffRole,
    TaskStatus,
    Timestamped,
    ZoneStatus,
)

# Stadium Models
from .stadium import (
    FoodCourt,
    Gate,
    ParkingArea,
    Washroom,
    Zone,
)

# People Models
from .people import (
    Fan,
    MedicalStaff,
    SecurityOfficer,
    Volunteer,
)

# Event Models
from .events import (
    AgentDecision,
    Alert,
    Incident,
    Prediction,
)

__all__ = [
    # Base
    "StadiumBaseModel",
    "Position",
    "Timestamped",
    "CrowdLevel",
    "ZoneStatus",
    "GateStatus",
    "IncidentSeverity",
    "IncidentType",
    "AlertLevel",
    "AgentType",
    "StaffRole",
    "RouteType",
    "TaskStatus",

    # Stadium
    "Zone",
    "Gate",
    "FoodCourt",
    "Washroom",
    "ParkingArea",

    # People
    "Fan",
    "Volunteer",
    "SecurityOfficer",
    "MedicalStaff",

    # Events
    "Incident",
    "Prediction",
    "Alert",
    "AgentDecision",
]