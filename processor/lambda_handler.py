from __future__ import annotations

import base64
import json
from pathlib import Path

from .config import load_processor_settings
from .repository import build_repository
from .service import EventProcessor

_SETTINGS = load_processor_settings()
_REPOSITORY = build_repository(_SETTINGS)
_PROCESSOR = EventProcessor(
    data_dir=Path(__file__).resolve().parents[1] / "data",
    repository=_REPOSITORY,
)


def lambda_handler(event: dict[str, object], _context: object) -> dict[str, object]:
    payloads = _extract_payloads(event)
    records = [_PROCESSOR.process_payload(payload) for payload in payloads]
    return {
        "processed_count": len(records),
        "records": records,
    }


def _extract_payloads(event: dict[str, object]) -> list[dict[str, object]]:
    if "Records" in event:
        records = event.get("Records")
        if not isinstance(records, list):
            raise ValueError("Records alani liste olmali.")
        return [_decode_kinesis_record(record) for record in records]

    if "payload" in event and isinstance(event["payload"], dict):
        return [event["payload"]]

    return [event]


def _decode_kinesis_record(record: object) -> dict[str, object]:
    if not isinstance(record, dict):
        raise ValueError("Kinesis record dict olmali.")

    kinesis = record.get("kinesis")
    if not isinstance(kinesis, dict):
        raise ValueError("Kinesis record icinde kinesis alani bulunamadi.")

    encoded_data = kinesis.get("data")
    if not isinstance(encoded_data, str):
        raise ValueError("Kinesis data alani string olmali.")

    decoded = base64.b64decode(encoded_data)
    return json.loads(decoded.decode("utf-8"))
