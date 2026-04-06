from __future__ import annotations

import re
from datetime import datetime, timezone

from .models import RawTelemetryEvent

BUS_ID_RE = re.compile(r"^BUS_[0-9]{3}_[0-9]{2}$")
LINE_ID_RE = re.compile(r"^LINE_[0-9]{3}$")
STOP_ID_RE = re.compile(r"^STOP_[A-Z0-9_]+$")
VALID_DIRECTIONS = {"outbound", "inbound"}


def parse_raw_event(payload: dict[str, object]) -> RawTelemetryEvent:
    _require_keys(
        payload,
        {
            "event_id",
            "timestamp",
            "bus_id",
            "line_id",
            "route_direction",
            "lat",
            "lon",
            "speed_kmh",
            "next_stop_id",
            "next_stop_name",
            "boarding_count",
        },
    )

    event_id = _expect_string(payload["event_id"], "event_id")
    timestamp_raw = _expect_string(payload["timestamp"], "timestamp")
    bus_id = _expect_string(payload["bus_id"], "bus_id")
    line_id = _expect_string(payload["line_id"], "line_id")
    route_direction = _expect_string(payload["route_direction"], "route_direction")
    next_stop_id = _expect_string(payload["next_stop_id"], "next_stop_id")
    next_stop_name = _expect_string(payload["next_stop_name"], "next_stop_name")

    if not BUS_ID_RE.match(bus_id):
        raise ValueError(f"Gecersiz bus_id: {bus_id}")
    if not LINE_ID_RE.match(line_id):
        raise ValueError(f"Gecersiz line_id: {line_id}")
    if route_direction not in VALID_DIRECTIONS:
        raise ValueError(f"Gecersiz route_direction: {route_direction}")
    if not STOP_ID_RE.match(next_stop_id):
        raise ValueError(f"Gecersiz next_stop_id: {next_stop_id}")
    if not next_stop_name.strip():
        raise ValueError("next_stop_name bos olamaz.")

    timestamp = _parse_timestamp(timestamp_raw)
    lat = _expect_number(payload["lat"], "lat", minimum=-90, maximum=90)
    lon = _expect_number(payload["lon"], "lon", minimum=-180, maximum=180)
    speed_kmh = _expect_number(payload["speed_kmh"], "speed_kmh", minimum=0, maximum=130)
    boarding_count = _expect_int(
        payload["boarding_count"],
        "boarding_count",
        minimum=0,
        maximum=20,
    )

    return RawTelemetryEvent(
        event_id=event_id,
        timestamp=timestamp,
        bus_id=bus_id,
        line_id=line_id,
        route_direction=route_direction,
        lat=lat,
        lon=lon,
        speed_kmh=speed_kmh,
        next_stop_id=next_stop_id,
        next_stop_name=next_stop_name,
        boarding_count=boarding_count,
    )


def _require_keys(payload: dict[str, object], required_keys: set[str]) -> None:
    missing = sorted(required_keys.difference(payload))
    if missing:
        raise ValueError(f"Eksik alanlar: {', '.join(missing)}")


def _expect_string(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} string olmalidir.")
    return value


def _expect_number(
    value: object,
    field_name: str,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field_name} sayi olmalidir.")
    numeric = float(value)
    if minimum is not None and numeric < minimum:
        raise ValueError(f"{field_name} minimum {minimum} olmali.")
    if maximum is not None and numeric > maximum:
        raise ValueError(f"{field_name} maksimum {maximum} olmali.")
    return numeric


def _expect_int(
    value: object,
    field_name: str,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field_name} integer olmalidir.")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field_name} minimum {minimum} olmali.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field_name} maksimum {maximum} olmali.")
    return value


def _parse_timestamp(raw_value: str) -> datetime:
    normalized = raw_value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"Gecersiz timestamp: {raw_value}") from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)

