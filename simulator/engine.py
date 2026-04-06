from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone

from .models import (
    BusState,
    DirectedRoute,
    DirectedSegment,
    Line,
    RouteDirection,
    SimulationCatalog,
    Stop,
)


class SimulationEngine:
    def __init__(
        self,
        catalog: SimulationCatalog,
        buses_per_line: int = 3,
        seed: int = 42,
    ) -> None:
        self.catalog = catalog
        self.random = random.Random(seed)
        self._route_cache: dict[tuple[str, RouteDirection], DirectedRoute] = {}
        self.buses = self._build_initial_fleet(buses_per_line)

    def step(self, observed_at: datetime, interval_seconds: int) -> list[dict[str, object]]:
        events: list[dict[str, object]] = []

        for bus in self.buses:
            self._advance_bus(bus, interval_seconds, observed_at)
            events.append(self._build_payload(bus, observed_at))

        return events

    def _build_initial_fleet(self, buses_per_line: int) -> list[BusState]:
        fleet: list[BusState] = []

        for line_id in sorted(self.catalog.lines):
            line = self.catalog.lines[line_id]
            outbound_route = self._get_directed_route(line, "outbound")

            for slot in range(buses_per_line):
                direction: RouteDirection = "outbound" if slot % 2 == 0 else "inbound"
                route = self._get_directed_route(line, direction)
                bus = self._new_bus_state(
                    bus_id=f"BUS_{line.public_code}_{slot + 1:02d}",
                    line=line,
                    route=route,
                )
                offset_seconds = int(outbound_route.cycle_seconds * slot / buses_per_line)
                if offset_seconds:
                    self._advance_bus(bus, offset_seconds, datetime.now(timezone.utc))
                fleet.append(bus)

        return fleet

    def _new_bus_state(self, bus_id: str, line: Line, route: DirectedRoute) -> BusState:
        first_segment = route.segments[0]
        segment_seconds = self._sample_segment_seconds(first_segment)
        speed_kmh = self._speed_for_segment(first_segment, segment_seconds)
        return BusState(
            bus_id=bus_id,
            line=line,
            route=route,
            phase="moving",
            current_stop_index=0,
            segment_progress=0.0,
            seconds_remaining_in_phase=0.0,
            current_segment_seconds=segment_seconds,
            speed_kmh=speed_kmh,
            pending_boarding_count=0,
        )

    def _advance_bus(self, bus: BusState, seconds: float, observed_at: datetime) -> None:
        remaining = float(seconds)

        while remaining > 0:
            if bus.phase == "moving":
                remaining = self._advance_moving_bus(bus, remaining, observed_at)
                continue

            remaining = self._advance_stationary_bus(bus, remaining)

    def _advance_moving_bus(
        self, bus: BusState, remaining: float, observed_at: datetime
    ) -> float:
        segment_remaining = (1.0 - bus.segment_progress) * bus.current_segment_seconds
        consumed = min(remaining, segment_remaining)
        bus.segment_progress += consumed / bus.current_segment_seconds
        remaining -= consumed

        if bus.segment_progress < 1.0:
            return remaining

        bus.segment_progress = 0.0
        bus.speed_kmh = 0.0
        bus.current_stop_index += 1
        bus.pending_boarding_count = self._sample_boarding_count(
            stop=bus.route.stops[bus.current_stop_index],
            observed_at=observed_at,
        )

        if bus.current_stop_index >= len(bus.route.stops) - 1:
            bus.phase = "terminal_wait"
            bus.seconds_remaining_in_phase = bus.route.default_terminal_wait_seconds
            return remaining

        bus.phase = "dwelling"
        bus.seconds_remaining_in_phase = bus.route.default_dwell_seconds
        return remaining

    def _advance_stationary_bus(self, bus: BusState, remaining: float) -> float:
        consumed = min(remaining, bus.seconds_remaining_in_phase)
        bus.seconds_remaining_in_phase -= consumed
        remaining -= consumed

        if bus.seconds_remaining_in_phase > 0:
            return remaining

        if bus.phase == "dwelling":
            self._start_next_segment(bus)
            return remaining

        self._reverse_direction(bus)
        return remaining

    def _start_next_segment(self, bus: BusState) -> None:
        bus.phase = "moving"
        next_segment = bus.route.segments[bus.current_stop_index]
        bus.current_segment_seconds = self._sample_segment_seconds(next_segment)
        bus.speed_kmh = self._speed_for_segment(next_segment, bus.current_segment_seconds)
        bus.segment_progress = 0.0

    def _reverse_direction(self, bus: BusState) -> None:
        new_direction: RouteDirection = (
            "inbound" if bus.route.direction == "outbound" else "outbound"
        )
        bus.route = self._get_directed_route(bus.line, new_direction)
        bus.current_stop_index = 0
        bus.phase = "moving"
        bus.segment_progress = 0.0
        next_segment = bus.route.segments[0]
        bus.current_segment_seconds = self._sample_segment_seconds(next_segment)
        bus.speed_kmh = self._speed_for_segment(next_segment, bus.current_segment_seconds)

    def _get_directed_route(self, line: Line, direction: RouteDirection) -> DirectedRoute:
        cache_key = (line.line_id, direction)
        cached = self._route_cache.get(cache_key)
        if cached is not None:
            return cached

        route_def = self.catalog.routes[line.line_id]
        if direction == "outbound":
            stops = tuple(self.catalog.stops[stop_id] for stop_id in route_def.stop_sequence)
            segments = tuple(
                DirectedSegment(
                    from_stop=self.catalog.stops[segment.from_stop_id],
                    to_stop=self.catalog.stops[segment.to_stop_id],
                    distance_km=segment.distance_km,
                    planned_seconds=segment.planned_seconds,
                )
                for segment in route_def.segments
            )
        else:
            reversed_stop_ids = tuple(reversed(route_def.stop_sequence))
            reversed_segments = tuple(reversed(route_def.segments))
            stops = tuple(self.catalog.stops[stop_id] for stop_id in reversed_stop_ids)
            segments = tuple(
                DirectedSegment(
                    from_stop=self.catalog.stops[segment.to_stop_id],
                    to_stop=self.catalog.stops[segment.from_stop_id],
                    distance_km=segment.distance_km,
                    planned_seconds=segment.planned_seconds,
                )
                for segment in reversed_segments
            )

        directed_route = DirectedRoute(
            line=line,
            direction=direction,
            stops=stops,
            segments=segments,
            default_dwell_seconds=route_def.default_dwell_seconds,
            default_terminal_wait_seconds=route_def.default_terminal_wait_seconds,
        )
        self._route_cache[cache_key] = directed_route
        return directed_route

    def _sample_segment_seconds(self, segment: DirectedSegment) -> float:
        multiplier = self.random.uniform(0.9, 1.18)
        return max(45.0, segment.planned_seconds * multiplier)

    def _speed_for_segment(self, segment: DirectedSegment, segment_seconds: float) -> float:
        return round((segment.distance_km / segment_seconds) * 3600, 1)

    def _sample_boarding_count(self, stop: Stop, observed_at: datetime) -> int:
        base_ranges = {
            "hub": (4, 9),
            "transfer": (3, 7),
            "terminal": (5, 10),
            "business": (1, 4),
            "residential": (1, 5),
            "civic": (1, 4),
            "education": (2, 5),
            "university": (3, 8),
            "campus": (2, 7),
        }
        low, high = base_ranges.get(stop.stop_type, (1, 4))
        hour = observed_at.astimezone(timezone.utc).hour
        multiplier = 1.25 if hour in {6, 7, 8, 16, 17, 18} else 1.0
        sampled = self.random.randint(low, high)
        if self.random.random() < 0.2:
            return 0
        return int(round(sampled * multiplier))

    def _build_payload(self, bus: BusState, observed_at: datetime) -> dict[str, object]:
        lat, lon = self._current_coordinates(bus)
        next_stop = self._next_stop(bus)
        payload = {
            "event_id": str(uuid.uuid4()),
            "timestamp": observed_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "bus_id": bus.bus_id,
            "line_id": bus.line.line_id,
            "route_direction": bus.route.direction,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "speed_kmh": round(bus.speed_kmh, 1),
            "next_stop_id": next_stop.stop_id,
            "next_stop_name": next_stop.name,
            "boarding_count": bus.pending_boarding_count,
        }
        bus.pending_boarding_count = 0
        return payload

    def _current_coordinates(self, bus: BusState) -> tuple[float, float]:
        if bus.phase != "moving":
            stop = bus.route.stops[bus.current_stop_index]
            return stop.lat, stop.lon

        segment = bus.route.segments[bus.current_stop_index]
        lat = segment.from_stop.lat + (
            (segment.to_stop.lat - segment.from_stop.lat) * bus.segment_progress
        )
        lon = segment.from_stop.lon + (
            (segment.to_stop.lon - segment.from_stop.lon) * bus.segment_progress
        )
        return lat, lon

    def _next_stop(self, bus: BusState) -> Stop:
        if bus.phase == "moving":
            return bus.route.segments[bus.current_stop_index].to_stop

        next_index = min(bus.current_stop_index + 1, len(bus.route.stops) - 1)
        return bus.route.stops[next_index]
