"""
=========================================================
events.py

Event models used throughout StadiumOS AI.

Responsibilities
----------------
- Incidents
- Predictions
- Alerts
- Agent Decisions

=========================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import Field

from .base import (
    AgentType,
    AlertLevel,
    IncidentSeverity,
    IncidentType,
    StadiumBaseModel,
)


# =========================================================
# Incident
# =========================================================

class Incident(StadiumBaseModel):
    """
    A real-time event occurring inside or around the stadium.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    type: IncidentType

    severity: IncidentSeverity

    zone_id: str

    description: str

    reported_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    resolved: bool = False


# =========================================================
# Prediction
# =========================================================

class Prediction(StadiumBaseModel):
    """
    AI prediction generated for a stadium zone.
    """

    zone_id: str

    predicted_crowd_density: float

    congestion_probability: float

    confidence: float

    reasoning: str

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


# =========================================================
# Alert
# =========================================================

class Alert(StadiumBaseModel):
    """
    Alert shown on the operations dashboard.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    level: AlertLevel

    title: str

    message: str

    zone_id: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    acknowledged: bool = False


# =========================================================
# Agent Decision
# =========================================================

class AgentDecision(StadiumBaseModel):
    """
    Recommendation produced by an AI agent.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    agent: AgentType

    zone_id: str

    recommendation: str

    priority: int = Field(ge=1, le=5)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    executed: bool = False