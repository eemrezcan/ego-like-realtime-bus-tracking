from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class ProcessorSettings:
    storage_mode: str
    aws_region: str | None
    dynamodb_endpoint_url: str | None
    current_state_table_name: str
    telemetry_history_table_name: str


def load_processor_settings() -> ProcessorSettings:
    base_dir = Path(__file__).resolve().parents[1]
    load_dotenv(base_dir / ".env")

    storage_mode = os.getenv("PROCESSOR_STORAGE_MODE", "memory").strip().lower()
    if storage_mode not in {"memory", "dynamodb"}:
        raise ValueError(
            "PROCESSOR_STORAGE_MODE yalnizca 'memory' veya 'dynamodb' olabilir."
        )

    aws_region = _optional_env("AWS_REGION")
    dynamodb_endpoint_url = _optional_env("DDB_ENDPOINT_URL")
    current_state_table_name = os.getenv("DDB_CURRENT_STATE_TABLE", "bus_current_state")
    telemetry_history_table_name = os.getenv(
        "DDB_HISTORY_TABLE",
        "telemetry_history",
    )

    return ProcessorSettings(
        storage_mode=storage_mode,
        aws_region=aws_region,
        dynamodb_endpoint_url=dynamodb_endpoint_url,
        current_state_table_name=current_state_table_name,
        telemetry_history_table_name=telemetry_history_table_name,
    )


def _optional_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None

