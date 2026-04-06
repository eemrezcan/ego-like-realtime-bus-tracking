from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RouteDirection = Literal["outbound", "inbound"]
BusPhase = Literal["moving", "dwelling", "terminal_wait"]


@dataclass(frozen=True)
class Stop:
    stop_id: str
    name: str
    district: str
    lat: float
    lon: float
    stop_type: str
    activity_tags: tuple[str, ...]


@dataclass(frozen=True)
class Line:
    line_id: str
    public_code: str
    name: str
    service_type: str
    color_hex: str
    vehicle_capacity: int
    nominal_headway_seconds: int
    service_start: str
    service_end: str


@dataclass(frozen=True)
class SegmentDefinition:
    from_stop_id: str
    to_stop_id: str
    distance_km: float
    planned_seconds: int


@dataclass(frozen=True)
class RouteDefinition:
    line_id: str
    route_name: str
    supports_reverse: bool
    terminal_stop_ids: tuple[str, str]
    default_dwell_seconds: int
    default_terminal_wait_seconds: int
    stop_sequence: tuple[str, ...]
    segments: tuple[SegmentDefinition, ...]


@dataclass(frozen=True)
class DirectedSegment:
    from_stop: Stop
    to_stop: Stop
    distance_km: float
    planned_seconds: int


@dataclass(frozen=True)
class DirectedRoute:
    line: Line
    direction: RouteDirection
    stops: tuple[Stop, ...]
    segments: tuple[DirectedSegment, ...]
    default_dwell_seconds: int
    default_terminal_wait_seconds: int

    @property
    def cycle_seconds(self) -> int:
        segment_seconds = sum(segment.planned_seconds for segment in self.segments)
        dwell_seconds = self.default_dwell_seconds * max(0, len(self.stops) - 2)
        return segment_seconds + dwell_seconds + self.default_terminal_wait_seconds


@dataclass(frozen=True)
class SimulationCatalog:
    lines: dict[str, Line]
    stops: dict[str, Stop]
    routes: dict[str, RouteDefinition]


@dataclass
class BusState:
    bus_id: str
    line: Line
    route: DirectedRoute
    phase: BusPhase
    current_stop_index: int
    segment_progress: float
    seconds_remaining_in_phase: float
    current_segment_seconds: float
    speed_kmh: float
    pending_boarding_count: int

