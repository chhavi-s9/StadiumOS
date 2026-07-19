"""
=========================================================
agents.py

Multi-Agent AI system for StadiumOS AI.

Responsibilities
----------------
- Crowd Agent
- Security Agent
- Volunteer Agent
- Coordinator Agent

=========================================================
"""

from __future__ import annotations

from app.llm import llm
from app.prompts import (
    CROWD_ANALYSIS_PROMPT,
    INCIDENT_RESPONSE_PROMPT,
    SUMMARY_PROMPT,
    VOLUNTEER_PROMPT,
)


# =========================================================
# Crowd Agent
# =========================================================

class CrowdAgent:
    """
    Analyzes crowd conditions and predicts congestion.
    """

    def analyze(
        self,
        zone: str,
        density: float,
        incidents: list[str],
    ) -> dict:

        prompt = CROWD_ANALYSIS_PROMPT.format(
            zone=zone,
            density=density,
            incidents=incidents,
        )

        result = llm.generate_json(
            prompt,
            task="prediction",
        )

        # If LLM failed or returned an error, provide a deterministic fallback
        if isinstance(result, dict) and result.get("error"):
            # Heuristic congestion risk
            if density > 0.9:
                risk = "critical"
                action = "Restrict entry; dispatch security; open alternate gates."
            elif density > 0.7:
                risk = "high"
                action = "Re-route flows; increase volunteer presence."
            elif density > 0.4:
                risk = "medium"
                action = "Monitor and advise gradual dispersal."
            else:
                risk = "low"
                action = "Normal operations."

            return {
                "zone": zone,
                "density": round(density, 2),
                "congestion_risk": risk,
                "recommendation": action,
                "incidents": incidents,
                "source": "heuristic_fallback",
            }

        return result


# =========================================================
# Security Agent
# =========================================================

class SecurityAgent:
    """
    Handles security and emergency incidents.
    """

    def analyze(
        self,
        incident_type: str,
        severity: str,
        location: str,
    ) -> dict:

        prompt = INCIDENT_RESPONSE_PROMPT.format(
            incident_type=incident_type,
            severity=severity,
            location=location,
        )

        return llm.generate_json(
            prompt,
            task="incident",
        )


# =========================================================
# Volunteer Agent
# =========================================================

class VolunteerAgent:
    """
    Assigns volunteers to stadium tasks.
    """

    def dispatch(
        self,
        task: str,
        volunteers: list[dict],
    ) -> dict:

        prompt = VOLUNTEER_PROMPT.format(
            task=task,
            volunteers=volunteers,
        )

        return llm.generate_json(
            prompt,
            task="volunteer",
        )


# =========================================================
# Coordinator Agent
# =========================================================

class CoordinatorAgent:
    """
    Generates an executive summary of the stadium.
    """

    def summarize(
        self,
        state: dict,
    ) -> str:

        prompt = SUMMARY_PROMPT.format(
            state=state,
        )

        try:
            return llm.generate(
                prompt,
                task="summary",
            )
        except Exception as exc:
            zones = state.get("zones", [])
            total_crowd = sum(z.get("current_occupancy", 0) for z in zones)
            incidents_count = len(state.get("incidents", []))
            return f"Executive Summary: Stadium operational. Total crowd count across {len(zones)} active zones is {total_crowd} fans with {incidents_count} active incident reports. (Note: Fallback summary active - {str(exc)})"


# =========================================================
# Agent Manager
# =========================================================

class AgentManager:
    """
    Central access point for all AI agents.
    """

    def __init__(self):

        self.crowd = CrowdAgent()

        self.security = SecurityAgent()

        self.volunteer = VolunteerAgent()

        self.coordinator = CoordinatorAgent()


agents = AgentManager()