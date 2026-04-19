from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Protocol

import boto3

from .config import ApiSettings


class ReadRepository(Protocol):
    def list_current_buses(self) -> list[dict[str, object]]:
        ...

    def get_bus(self, bus_id: str) -> dict[str, object] | None:
        ...


class JsonlReadRepository:
    def __init__(self, source_file: Path) -> None:
        self._source_file = source_file

    def list_current_buses(self) -> list[dict[str, object]]:
        events = self._load_events()
        latest_by_bus: dict[str, dict[str, object]] = {}

        for event in events:
            bus_id = str(event["bus_id"])
            current = latest_by_bus.get(bus_id)
            if current is None or str(event["timestamp"]) >= str(current["timestamp"]):
                latest_by_bus[bus_id] = event

        return list(latest_by_bus.values())

    def get_bus(self, bus_id: str) -> dict[str, object] | None:
        buses = self.list_current_buses()
        for bus in buses:
            if bus.get("bus_id") == bus_id:
                return bus
        return None

    def _load_events(self) -> list[dict[str, object]]:
        if not self._source_file.exists():
            return []

        content = self._source_file.read_text(encoding="utf-8").strip()
        if not content:
            return []

        events: list[dict[str, object]] = []
        for line in content.splitlines():
            if not line.strip():
                continue
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                events.append(parsed)
        return events


class DynamoDbReadRepository:
    def __init__(self, settings: ApiSettings) -> None:
        if not settings.aws_region:
            raise ValueError("DynamoDB modu icin AWS_REGION zorunludur.")

        session = boto3.session.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )
        dynamodb = session.resource(
            "dynamodb",
            endpoint_url=settings.dynamodb_endpoint_url,
        )
        self._current_state_table = dynamodb.Table(settings.current_state_table_name)

    def list_current_buses(self) -> list[dict[str, object]]:
        response = self._current_state_table.scan()
        return [_deserialize_item(item) for item in response.get("Items", [])]

    def get_bus(self, bus_id: str) -> dict[str, object] | None:
        response = self._current_state_table.get_item(Key={"bus_id": bus_id})
        item = response.get("Item")
        return _deserialize_item(item) if item else None


def build_read_repository(settings: ApiSettings) -> ReadRepository:
    if settings.storage_mode == "dynamodb":
        return DynamoDbReadRepository(settings)
    return JsonlReadRepository(settings.enriched_events_file)


def _deserialize_item(item: dict[str, object]) -> dict[str, object]:
    return {key: _deserialize_value(value) for key, value in item.items()}


def _deserialize_value(value: object) -> object:
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    if isinstance(value, dict):
        return {key: _deserialize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_deserialize_value(item) for item in value]
    return value
