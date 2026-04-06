from __future__ import annotations

import json
from pathlib import Path

from .models import Line, RouteDefinition, SegmentDefinition, SimulationCatalog, Stop


def load_catalog(data_dir: Path) -> SimulationCatalog:
    lines = _load_lines(data_dir / "lines.json")
    stops = _load_stops(data_dir / "stops.json")
    routes = _load_routes(data_dir / "routes.json")

    for route in routes.values():
        if route.line_id not in lines:
            raise ValueError(f"Route {route.line_id} references an unknown line.")
        _validate_route(route, stops)

    return SimulationCatalog(lines=lines, stops=stops, routes=routes)


def _load_lines(path: Path) -> dict[str, Line]:
    raw_lines = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["line_id"]: Line(
            line_id=item["line_id"],
            public_code=item["public_code"],
            name=item["name"],
            service_type=item["service_type"],
            color_hex=item["color_hex"],
            vehicle_capacity=item["vehicle_capacity"],
            nominal_headway_seconds=item["nominal_headway_seconds"],
            service_start=item["service_start"],
            service_end=item["service_end"],
        )
        for item in raw_lines
    }


def _load_stops(path: Path) -> dict[str, Stop]:
    raw_stops = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["stop_id"]: Stop(
            stop_id=item["stop_id"],
            name=item["name"],
            district=item["district"],
            lat=item["lat"],
            lon=item["lon"],
            stop_type=item["stop_type"],
            activity_tags=tuple(item["activity_tags"]),
        )
        for item in raw_stops
    }


def _load_routes(path: Path) -> dict[str, RouteDefinition]:
    raw_routes = json.loads(path.read_text(encoding="utf-8"))
    routes: dict[str, RouteDefinition] = {}

    for item in raw_routes:
        routes[item["line_id"]] = RouteDefinition(
            line_id=item["line_id"],
            route_name=item["route_name"],
            supports_reverse=item["supports_reverse"],
            terminal_stop_ids=tuple(item["terminal_stop_ids"]),
            default_dwell_seconds=item["default_dwell_seconds"],
            default_terminal_wait_seconds=item["default_terminal_wait_seconds"],
            stop_sequence=tuple(item["stop_sequence"]),
            segments=tuple(
                SegmentDefinition(
                    from_stop_id=segment["from_stop_id"],
                    to_stop_id=segment["to_stop_id"],
                    distance_km=segment["distance_km"],
                    planned_seconds=segment["planned_seconds"],
                )
                for segment in item["segments"]
            ),
        )

    return routes


def _validate_route(route: RouteDefinition, stops: dict[str, Stop]) -> None:
    if len(route.stop_sequence) < 2:
        raise ValueError(f"Route {route.line_id} must have at least two stops.")

    for stop_id in route.stop_sequence:
        if stop_id not in stops:
            raise ValueError(f"Route {route.line_id} references unknown stop {stop_id}.")

    if len(route.segments) != len(route.stop_sequence) - 1:
        raise ValueError(
            f"Route {route.line_id} must have exactly one segment per stop pair."
        )

    for index, segment in enumerate(route.segments):
        expected_from = route.stop_sequence[index]
        expected_to = route.stop_sequence[index + 1]
        if segment.from_stop_id != expected_from or segment.to_stop_id != expected_to:
            raise ValueError(
                f"Route {route.line_id} has a segment order mismatch at index {index}."
            )

