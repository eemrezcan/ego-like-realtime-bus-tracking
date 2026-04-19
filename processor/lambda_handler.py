from __future__ import annotations

import base64
import json
import logging
from pathlib import Path

from .config import load_processor_settings
from .repository import build_repository
from .service import EventProcessor

LOGGER = logging.getLogger(__name__)
_SETTINGS = load_processor_settings()
_REPOSITORY = build_repository(_SETTINGS)
_PROCESSOR = EventProcessor(
    data_dir=Path(__file__).resolve().parents[1] / "data",
    repository=_REPOSITORY,
)


def lambda_handler(event: dict[str, object], _context: object) -> dict[str, object]:
    payloads = _extract_payloads(event)
    records: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []

    for payload in payloads:
        try:
            records.append(_PROCESSOR.process_payload(payload))
        except Exception as exc:  # pragma: no cover - exercised in Lambda/runtime tests.
            bus_id = payload.get("bus_id") if isinstance(payload, dict) else None
            LOGGER.exception("Payload islenemedi. bus_id=%s", bus_id)
            failures.append(
                {
                    "bus_id": bus_id,
                    "error": str(exc),
                }
            )

    return {
        "processed_count": len(records),
        "failed_count": len(failures),
        "records": records,
        "failures": failures,
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
