"""
Simple demo runner: simulates surge and auto-executes planner actions, returning a timeline.
"""
from typing import Any, Dict, List
import time
from app.simulation import simulation
from app.planner import plan_actions


def run_demo(steps: int = 4, interval: float = 1.0) -> List[Dict[str, Any]]:
    timeline = []

    # baseline state
    timeline.append({"t": 0, "state": simulation.state(), "actions": []})

    # Simple surge values (occupancies)
    surge_values = [500, 1500, 3000, 4200][:steps]

    for i, occ in enumerate(surge_values, start=1):
        # apply occupancy updates to first three zones
        for idx, zid in enumerate(["Z1", "Z2", "Z3"]):
            zone = next((z for z in simulation.zones if z.id == zid), None)
            if zone:
                # stagger occupancy
                mult = 1.0 - (idx * 0.2)
                zone.current_occupancy = int(occ * mult)

        # tick simulation
        simulation.tick()

        # plan
        state = simulation.state()
        actions = plan_actions(state)

        executed = []
        from app.models import Incident, IncidentType, IncidentSeverity
        for a in actions:
            target_zone = a.get("zone_id", "Z1")
            inc = Incident(
                type=IncidentType.CROWD_SURGE,
                severity=IncidentSeverity.MEDIUM,
                zone_id=target_zone,
                description=f"Action: {a.get('message', 'Demo Action')}"
            )
            simulation.incidents.append(inc)
            executed.append(a)

        timeline.append({"t": i, "state": state, "actions": executed})

        time.sleep(interval)

    return timeline
