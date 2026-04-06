from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

import boto3

from .config import ProcessorSettings
from .models import EnrichedTelemetryEvent


@dataclass(frozen=True)
class BusComputedState:
    occupancy_score: int
    estimated_eta_sec: int
    estimated_occupancy_level: str
    timestamp: str


class TelemetryRepository(Protocol):
    def get_current_state(self, bus_id: str) -> BusComputedState | None:
        ...

    def persist_event(self, event: EnrichedTelemetryEvent) -> None:
        ...


class InMemoryTelemetryRepository:
    def __init__(self) -> None:
        self._current_state: dict[str, BusComputedState] = {}
        self.history: list[dict[str, object]] = []

    def get_current_state(self, bus_id: str) -> BusComputedState | None:
        return self._current_state.get(bus_id)

    def persist_event(self, event: EnrichedTelemetryEvent) -> None:
        self._current_state[event.bus_id] = BusComputedState(
            occupancy_score=event.estimated_occupancy_score,
            estimated_eta_sec=event.estimated_eta_sec,
            estimated_occupancy_level=event.estimated_occupancy_level,
            timestamp=event.timestamp,
        )
        self.history.append(event.to_dict())


class DynamoDbTelemetryRepository:
    def __init__(
        self,
        settings: ProcessorSettings,
    ) -> None:
        if not settings.aws_region:
            raise ValueError("DynamoDB modu icin AWS_REGION zorunludur.")

        session = boto3.session.Session(region_name=settings.aws_region)
        dynamodb = session.resource(
            "dynamodb",
            endpoint_url=settings.dynamodb_endpoint_url,
        )
        self._current_state_table = dynamodb.Table(settings.current_state_table_name)
        self._history_table = dynamodb.Table(settings.telemetry_history_table_name)

    def get_current_state(self, bus_id: str) -> BusComputedState | None:
        response = self._current_state_table.get_item(Key={"bus_id": bus_id})
        item = response.get("Item")
        if not item:
            return None

        return BusComputedState(
            occupancy_score=int(item.get("estimated_occupancy_score", 0)),
            estimated_eta_sec=int(item.get("estimated_eta_sec", 0)),
            estimated_occupancy_level=str(item.get("estimated_occupancy_level", "dusuk")),
            timestamp=str(item.get("timestamp", "")),
        )

    def persist_event(self, event: EnrichedTelemetryEvent) -> None:
        current_state_item = _serialize_for_dynamodb(
            {
                "bus_id": event.bus_id,
                "timestamp": event.timestamp,
                "event_id": event.event_id,
                "line_id": event.line_id,
                "route_direction": event.route_direction,
                "lat": event.lat,
                "lon": event.lon,
                "speed_kmh": event.speed_kmh,
                "next_stop_id": event.next_stop_id,
                "next_stop_name": event.next_stop_name,
                "boarding_count": event.boarding_count,
                "estimated_eta_sec": event.estimated_eta_sec,
                "estimated_alighting_count": event.estimated_alighting_count,
                "estimated_occupancy_score": event.estimated_occupancy_score,
                "estimated_occupancy_level": event.estimated_occupancy_level,
                "is_delayed": event.is_delayed,
            }
        )
        history_item = _serialize_for_dynamodb(event.to_dict())

        self._current_state_table.put_item(Item=current_state_item)
        self._history_table.put_item(Item=history_item)


def build_repository(settings: ProcessorSettings) -> TelemetryRepository:
    if settings.storage_mode == "dynamodb":
        return DynamoDbTelemetryRepository(settings)
    return InMemoryTelemetryRepository()


def _serialize_for_dynamodb(value: object) -> object:
    if isinstance(value, bool):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {key: _serialize_for_dynamodb(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize_for_dynamodb(item) for item in value]
    return value
