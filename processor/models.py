from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class RawTelemetryEvent:
    event_id: str
    timestamp: datetime
    bus_id: str
    line_id: str
    route_direction: str
    lat: float
    lon: float
    speed_kmh: float
    next_stop_id: str
    next_stop_name: str
    boarding_count: int


@dataclass(frozen=True)
class EnrichedTelemetryEvent:
    event_id: str
    timestamp: str
    bus_id: str
    line_id: str
    route_direction: str
    lat: float
    lon: float
    speed_kmh: float
    next_stop_id: str
    next_stop_name: str
    boarding_count: int
    estimated_eta_sec: int
    estimated_alighting_count: int
    estimated_occupancy_score: int
    estimated_occupancy_level: str
    is_delayed: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

