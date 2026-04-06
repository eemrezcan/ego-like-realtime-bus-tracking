from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    storage_mode: str
    current_bus_count: int
    configured_line_count: int
    configured_stop_count: int


class BusStateResponse(BaseModel):
    bus_id: str
    line_id: str
    line_name: str
    route_direction: str
    timestamp: str
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


class LineSummaryResponse(BaseModel):
    line_id: str
    public_code: str
    name: str
    active_bus_count: int
    average_speed_kmh: float
    average_eta_sec: int
    delayed_bus_count: int
    occupancy_low_count: int
    occupancy_medium_count: int
    occupancy_high_count: int


class SystemSummaryResponse(BaseModel):
    total_buses: int
    total_lines: int
    delayed_bus_count: int
    average_speed_kmh: float
    occupancy_low_count: int
    occupancy_medium_count: int
    occupancy_high_count: int
    latest_timestamp: str | None

