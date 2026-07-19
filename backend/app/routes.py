"""
=========================================================
routes.py

REST API routes for StadiumOS AI.

Responsibilities
----------------
- Health Check
- Stadium State
- Predictions
- Incidents
- AI Summary

=========================================================
"""

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.agents import agents
from app.simulation import simulation
from app.planner import plan_actions
from app.demo_runner import run_demo

from typing import List, Dict, Any

router = APIRouter()


# =========================================================
# Health
# =========================================================

@router.get("/health")
def health():
    return {
        "status": "online",
        "service": "StadiumOS AI",
    }


# =========================================================
# Live Stadium State
# =========================================================

@router.get("/state")
def state():

    simulation.tick()

    return simulation.state()


# =========================================================
# Predictions
# =========================================================

@router.get("/predictions")
def predictions():

    simulation.tick()

    return [
    prediction.model_dump()
    for prediction in simulation.predictions
    ]


# =========================================================
# Incidents
# =========================================================

@router.get("/incidents")
def incidents():

    simulation.tick()

    return [
    incident.model_dump()
    for incident in simulation.incidents
    ]


# =========================================================
# Sensor ingest
# =========================================================


@router.post("/ingest/heatmap")
def ingest_heatmap(payload: Dict[str, Any] = Body(...)):
    """Accepts zone occupancy updates: {"zone_updates":[{"zone_id":"Z1","occupancy":123},...]}
    """
    updates = payload.get("zone_updates", [])
    for u in updates:
        zid = u.get("zone_id")
        occ = int(u.get("occupancy", 0))
        zone = next((z for z in simulation.zones if z.id == zid), None)
        if zone:
            zone.current_occupancy = occ
    return {"status": "ok", "updated": len(updates)}


# =========================================================
# Planner & Action endpoints
# =========================================================


@router.get("/plan")
def get_plan():
    simulation.tick()
    state = simulation.state()
    actions = plan_actions(state)
    return {"actions": actions}


@router.post("/actions/execute")
def execute_action(action: Dict[str, Any] = Body(...)):
    from app.models import Incident, IncidentType, IncidentSeverity
    target_zone = action.get("zone_id", "Z1")
    inc = Incident(
        type=IncidentType.CROWD_SURGE,
        severity=IncidentSeverity.MEDIUM,
        zone_id=target_zone,
        description=f"Action executed: {action.get('message', 'Custom Action')}"
    )
    simulation.incidents.append(inc)
    return {"status": "executed", "action": action}



@router.post('/demo/run')
def demo_run(steps: int = 4):
    """Run an automated demo: simulate surges, plan and execute actions, return timeline."""
    timeline = run_demo(steps=steps, interval=0.5)
    # convert objects to JSON-friendly
    out = []
    for item in timeline:
        zones = []
        for z in item['state'].get('zones', []):
            if hasattr(z, 'model_dump'):
                zones.append(z.model_dump())
            else:
                zones.append(z)

        out.append({
            't': item['t'],
            'zones': zones,
            'actions': item['actions']
        })
    return {'timeline': out}


# =========================================================
# AI Executive Summary
# =========================================================

@router.get("/summary")
def summary():

    print("1. Route hit")

    simulation.tick()

    print("2. Simulation complete")

    result = agents.coordinator.summarize(
        simulation.state()
    )

    print("3. LLM returned")

    return {
        "summary": result
    }

# =========================================================
# Crowd Analysis
# =========================================================

@router.get("/zones/{zone_id}/analysis")
def analyze_zone(zone_id: str):

    simulation.tick()

    zone = next(
        (
            z
            for z in simulation.zones
            if z.id == zone_id
        ),
        None,
    )

    if zone is None:
        return {"error": "Zone not found"}

    incidents = [
        i.type.value
        for i in simulation.incidents
        if i.zone_id == zone_id
    ]

    result = agents.crowd.analyze(
        zone=zone.name,
        density=zone.current_occupancy / zone.capacity,
        incidents=incidents,
    )

    if isinstance(result, dict) and result.get("error"):
        return JSONResponse(
            status_code=502,
            content={
                "error": "Crowd analysis failed",
                "details": result.get("details", result.get("error")),
            },
        )

    return result