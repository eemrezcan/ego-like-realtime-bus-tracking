from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - Optional in non-local runtimes.
    def load_dotenv(*_args: object, **_kwargs: object) -> bool:
        return False


@dataclass(frozen=True)
class ApiSettings:
    storage_mode: str
    aws_region: str | None
    dynamodb_endpoint_url: str | None
    current_state_table_name: str
    enriched_events_file: Path


def load_api_settings() -> ApiSettings:
    base_dir = Path(__file__).resolve().parents[1]
    load_dotenv(base_dir / ".env")

    storage_mode = os.getenv("API_STORAGE_MODE", "jsonl").strip().lower()
    if storage_mode not in {"jsonl", "dynamodb"}:
        raise ValueError("API_STORAGE_MODE yalnizca 'jsonl' veya 'dynamodb' olabilir.")

    enriched_events_file = Path(
        os.getenv("API_ENRICHED_EVENTS_FILE", "output/enriched-telemetry.jsonl")
    )
    if not enriched_events_file.is_absolute():
        enriched_events_file = base_dir / enriched_events_file

    return ApiSettings(
        storage_mode=storage_mode,
        aws_region=_optional_env("AWS_REGION"),
        dynamodb_endpoint_url=_optional_env("DDB_ENDPOINT_URL"),
        current_state_table_name=os.getenv("DDB_CURRENT_STATE_TABLE", "bus_current_state"),
        enriched_events_file=enriched_events_file,
    )


def _optional_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
