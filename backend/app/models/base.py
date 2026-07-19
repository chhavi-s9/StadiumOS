"""
=========================================================
base.py

Shared domain types for StadiumOS AI.

Responsibilities
----------------
- Common enums
- Shared status types
- Reusable value objects
- Base model configuration

All domain models inherit or import from this module.

=========================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# Base Model
# =========================================================

class StadiumBaseModel(BaseModel):
    """
    Base class for all Pydantic models.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


# =========================================================
# Shared Value Objects
# =========================================================

class Position(StadiumBaseModel):
    """
    2D coordinate inside the stadium map.
    """

    x: float
    y: float
    floor: int = 0


class Timestamped(StadiumBaseModel):
    """
    Adds timestamps to any model.
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# =========================================================
# Crowd
# =========================================================

class CrowdLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# =========================================================
# Zone Status
# =========================================================

class ZoneStatus(StrEnum):
    OPEN = "OPEN"
    BUSY = "BUSY"
    RESTRICTED = "RESTRICTED"
    CLOSED = "CLOSED"


# =========================================================
# Gate Status
# =========================================================

class GateStatus(StrEnum):
    OPEN = "OPEN"
    QUEUEING = "QUEUEING"
    FULL = "FULL"
    CLOSED = "CLOSED"


# =========================================================
# Incident
# =========================================================

class IncidentSeverity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentType(StrEnum):
    CONGESTION = "CONGESTION"
    MEDICAL = "MEDICAL"
    SECURITY = "SECURITY"
    LOST_CHILD = "LOST_CHILD"
    ACCESSIBILITY = "ACCESSIBILITY"
    FIRE = "FIRE"
    WEATHER = "WEATHER"
    VIP = "VIP"


# =========================================================
# Alerts
# =========================================================

class AlertLevel(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


# =========================================================
# AI Agents
# =========================================================

class AgentType(StrEnum):
    CROWD = "CROWD"
    SECURITY = "SECURITY"
    VOLUNTEER = "VOLUNTEER"
    MEDICAL = "MEDICAL"
    ACCESSIBILITY = "ACCESSIBILITY"
    TRANSPORT = "TRANSPORT"
    COORDINATOR = "COORDINATOR"


# =========================================================
# Staff Roles
# =========================================================

class StaffRole(StrEnum):
    VOLUNTEER = "VOLUNTEER"
    SECURITY = "SECURITY"
    MEDICAL = "MEDICAL"
    OPERATIONS = "OPERATIONS"


# =========================================================
# Route Types
# =========================================================

class RouteType(StrEnum):
    NORMAL = "NORMAL"
    ACCESSIBLE = "ACCESSIBLE"
    EMERGENCY = "EMERGENCY"
    VIP = "VIP"


# =========================================================
# Task Status
# =========================================================

class TaskStatus(StrEnum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"