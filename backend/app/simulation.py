"""
=========================================================
simulation.py

Live stadium simulation engine.

Responsibilities
----------------
- Simulate fan movement
- Update crowd levels
- Generate random incidents
- Maintain stadium state

=========================================================
"""

from __future__ import annotations

import random

from app.models import (
    AlertLevel,
    CrowdLevel,
    Fan,
    Incident,
    IncidentSeverity,
    IncidentType,
    Position,
    Prediction,
    Zone,
    ZoneStatus,
)


class StadiumSimulation:
    """
    Simulates a live FIFA stadium.
    """

    def __init__(self):

        self.zones = self._create_zones()

        self.fans = self._create_fans()

        self.incidents: list[Incident] = []

        self.predictions: list[Prediction] = []

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def _create_zones(self):

        zones = []

        for i in range(1, 9):

            zones.append(
                Zone(
                    id=f"Z{i}",
                    name=f"Zone {i}",
                    position=Position(
                        x=random.randint(0, 100),
                        y=random.randint(0, 100),
                    ),
                    capacity=5000,
                )
            )

        return zones

    def _create_fans(self):

        fans = []

        zone_ids = [z.id for z in self.zones]

        for i in range(500):

            zone = random.choice(zone_ids)

            fans.append(
                Fan(
                    id=f"fan_{i}",
                    ticket_id=f"TKT{i}",
                    current_zone=zone,
                    destination_zone=random.choice(zone_ids),
                    position=Position(
                        x=random.randint(0, 100),
                        y=random.randint(0, 100),
                    ),
                )
            )

        return fans

    # =====================================================
    # FAN MOVEMENT
    # =====================================================

    def move_fans(self):

        zone_ids = [z.id for z in self.zones]

        for fan in self.fans:

            if random.random() < 0.05:

                fan.current_zone = random.choice(zone_ids)

    # =====================================================
    # CROWD UPDATE
    # =====================================================

    def update_zones(self):

        for zone in self.zones:

            occupancy = sum(
                1
                for fan in self.fans
                if fan.current_zone == zone.id
            )

            zone.current_occupancy = occupancy

            ratio = occupancy / zone.capacity

            if ratio > 0.90:
                zone.crowd_level = CrowdLevel.CRITICAL
                zone.status = ZoneStatus.RESTRICTED

            elif ratio > 0.70:
                zone.crowd_level = CrowdLevel.HIGH
                zone.status = ZoneStatus.BUSY

            elif ratio > 0.40:
                zone.crowd_level = CrowdLevel.MEDIUM
                zone.status = ZoneStatus.OPEN

            else:
                zone.crowd_level = CrowdLevel.LOW
                zone.status = ZoneStatus.OPEN

    # =====================================================
    # INCIDENTS
    # =====================================================

    def generate_incidents(self):

        if random.random() > 0.97:

            zone = random.choice(self.zones)

            incident = Incident(
                type=random.choice(list(IncidentType)),
                severity=random.choice(list(IncidentSeverity)),
                zone_id=zone.id,
                description="Automatically simulated event",
            )

            self.incidents.append(incident)

    # =====================================================
    # PREDICTIONS
    # =====================================================

    def generate_predictions(self):

        self.predictions = []

        for zone in self.zones:

            density = zone.current_occupancy / zone.capacity

            self.predictions.append(
                Prediction(
                    zone_id=zone.id,
                    predicted_crowd_density=round(density, 2),
                    congestion_probability=min(
                        1.0,
                        density + random.uniform(0, 0.2),
                    ),
                    confidence=0.92,
                    reasoning="Simulation-based estimation",
                )
            )

    # =====================================================
    # TICK
    # =====================================================

    def tick(self):

        self.move_fans()

        self.update_zones()

        self.generate_incidents()

        self.generate_predictions()

    # =====================================================
    # EXPORT STATE
    # =====================================================

    def state(self):

        return {
        "zones": [
            zone.model_dump()
            for zone in self.zones
        ],
        "fans": [
            fan.model_dump()
            for fan in self.fans
        ],
        "incidents": [
            incident.model_dump()
            for incident in self.incidents
        ],
        "predictions": [
            prediction.model_dump()
            for prediction in self.predictions
        ],
    }

simulation = StadiumSimulation()