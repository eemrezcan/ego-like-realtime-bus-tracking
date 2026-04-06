from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from simulator.data_loader import load_catalog
from simulator.models import SimulationCatalog

from .eta import estimate_eta_seconds, estimate_planned_remaining_seconds, haversine_km
from .models import EnrichedTelemetryEvent, RawTelemetryEvent
from .occupancy import (
    classify_occupancy_level,
    compute_occupancy_score,
    estimate_alighting_count,
)
from .repository import InMemoryTelemetryRepository, TelemetryRepository
from .validators import parse_raw_event


@dataclass(frozen=True)
class RouteStopContext:
    stop_type: str
    stop_index: int
    total_stops: int
    segment_distance_km: float
    segment_planned_seconds: int
    stop_lat: float
    stop_lon: float
    vehicle_capacity: int


class EventProcessor:
    def __init__(
        self,
        data_dir: Path | None = None,
        repository: TelemetryRepository | None = None,
    ) -> None:
        base_dir = Path(__file__).resolve().parents[1]
        self.catalog = load_catalog(data_dir or (base_dir / "data"))
        self.repository = repository or InMemoryTelemetryRepository()
        self._route_context = self._build_route_context(self.catalog)

    def process_payload(self, payload: dict[str, object]) -> dict[str, object]:
        event = parse_raw_event(payload)
        enriched = self._enrich_event(event)
        return enriched.to_dict()

    def _enrich_event(self, event: RawTelemetryEvent) -> EnrichedTelemetryEvent:
        context_key = (event.line_id, event.route_direction, event.next_stop_id)
        route_context = self._route_context.get(context_key)
        if route_context is None:
            raise ValueError(
                f"Rota baglami bulunamadi: line_id={event.line_id}, "
                f"route_direction={event.route_direction}, next_stop_id={event.next_stop_id}"
            )

        distance_remaining_km = haversine_km(
            event.lat,
            event.lon,
            route_context.stop_lat,
            route_context.stop_lon,
        )
        planned_remaining_seconds = estimate_planned_remaining_seconds(
            distance_remaining_km=distance_remaining_km,
            segment_distance_km=route_context.segment_distance_km,
            segment_planned_seconds=route_context.segment_planned_seconds,
        )
        estimated_eta_sec = estimate_eta_seconds(
            distance_remaining_km=distance_remaining_km,
            current_speed_kmh=event.speed_kmh,
            planned_remaining_seconds=planned_remaining_seconds,
        )

        previous_state = self.repository.get_current_state(event.bus_id)
        previous_occupancy = previous_state.occupancy_score if previous_state is not None else 0
        estimated_alighting = estimate_alighting_count(
            previous_occupancy=previous_occupancy,
            boarding_count=event.boarding_count,
            stop_type=route_context.stop_type,
            stop_position_index=route_context.stop_index,
            total_stops=route_context.total_stops,
        )
        estimated_occupancy = compute_occupancy_score(
            previous_occupancy=previous_occupancy,
            boarding_count=event.boarding_count,
            estimated_alighting_count=estimated_alighting,
            vehicle_capacity=route_context.vehicle_capacity,
        )
        estimated_level = classify_occupancy_level(
            occupancy_score=estimated_occupancy,
            vehicle_capacity=route_context.vehicle_capacity,
        )
        is_delayed = (estimated_eta_sec - planned_remaining_seconds) >= 90

        enriched_event = EnrichedTelemetryEvent(
            event_id=event.event_id,
            timestamp=event.timestamp.isoformat().replace("+00:00", "Z"),
            bus_id=event.bus_id,
            line_id=event.line_id,
            route_direction=event.route_direction,
            lat=round(event.lat, 6),
            lon=round(event.lon, 6),
            speed_kmh=round(event.speed_kmh, 1),
            next_stop_id=event.next_stop_id,
            next_stop_name=event.next_stop_name,
            boarding_count=event.boarding_count,
            estimated_eta_sec=estimated_eta_sec,
            estimated_alighting_count=estimated_alighting,
            estimated_occupancy_score=estimated_occupancy,
            estimated_occupancy_level=estimated_level,
            is_delayed=is_delayed,
        )
        self.repository.persist_event(enriched_event)
        return enriched_event

    def _build_route_context(
        self,
        catalog: SimulationCatalog,
    ) -> dict[tuple[str, str, str], RouteStopContext]:
        context: dict[tuple[str, str, str], RouteStopContext] = {}

        for line_id, route_def in catalog.routes.items():
            line = catalog.lines[line_id]

            outbound_stops = route_def.stop_sequence
            for index, segment in enumerate(route_def.segments, start=1):
                stop_id = outbound_stops[index]
                stop = catalog.stops[stop_id]
                context[(line_id, "outbound", stop_id)] = RouteStopContext(
                    stop_type=stop.stop_type,
                    stop_index=index,
                    total_stops=len(outbound_stops),
                    segment_distance_km=segment.distance_km,
                    segment_planned_seconds=segment.planned_seconds,
                    stop_lat=stop.lat,
                    stop_lon=stop.lon,
                    vehicle_capacity=line.vehicle_capacity,
                )

            inbound_stops = tuple(reversed(route_def.stop_sequence))
            reversed_segments = tuple(reversed(route_def.segments))
            for index, segment in enumerate(reversed_segments, start=1):
                stop_id = inbound_stops[index]
                stop = catalog.stops[stop_id]
                context[(line_id, "inbound", stop_id)] = RouteStopContext(
                    stop_type=stop.stop_type,
                    stop_index=index,
                    total_stops=len(inbound_stops),
                    segment_distance_km=segment.distance_km,
                    segment_planned_seconds=segment.planned_seconds,
                    stop_lat=stop.lat,
                    stop_lon=stop.lon,
                    vehicle_capacity=line.vehicle_capacity,
                )

        return context
