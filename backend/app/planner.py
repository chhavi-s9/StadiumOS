"""
Simple rule-based planner for MVP.
"""
from typing import List, Dict, Any


def plan_actions(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    actions = []
    zones = state.get("zones", [])

    for z in zones:
        zid = z.get("id")
        occ = z.get("current_occupancy", 0)
        cap = z.get("capacity", 1)
        density = occ / cap if cap else 0

        if density > 0.9:
            actions.append({
                "id": f"restrict_{zid}",
                "zone_id": zid,
                "type": "restrict_entry",
                "priority": "critical",
                "message": f"High density in {zid} ({density:.2f}). Restrict entry and deploy security.",
                "expected_effect": "reduce_density",
            })
        elif density > 0.7:
            actions.append({
                "id": f"reroute_{zid}",
                "zone_id": zid,
                "type": "reroute",
                "priority": "high",
                "message": f"Elevated density in {zid} ({density:.2f}). Re-route volunteers and open adjacent gates.",
                "expected_effect": "flatten_flow",
            })
        elif density > 0.4:
            actions.append({
                "id": f"monitor_{zid}",
                "zone_id": zid,
                "type": "monitor",
                "priority": "medium",
                "message": f"Moderate density in {zid} ({density:.2f}). Increase monitoring.",
                "expected_effect": "observe",
            })

    # Global actions: if many zones high, propose exit smoothing
    high_count = sum(1 for z in zones if (z.get("current_occupancy",0)/z.get("capacity",1))>0.7)
    if high_count >= 3:
        actions.insert(0,{
            "id":"egress_phase_1",
            "type":"egress_smoothing",
            "priority":"high",
            "message":"Multiple zones showing high density — initiate phased egress plan.",
            "expected_effect":"smooth_egress",
        })

    return actions
