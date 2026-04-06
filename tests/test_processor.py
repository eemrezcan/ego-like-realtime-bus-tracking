from __future__ import annotations

import base64
import json
import unittest
from pathlib import Path

from processor.lambda_handler import lambda_handler
from processor.repository import InMemoryTelemetryRepository
from processor.service import EventProcessor


class ProcessorTests(unittest.TestCase):
    def setUp(self) -> None:
        data_dir = Path(__file__).resolve().parents[1] / "data"
        self.repository = InMemoryTelemetryRepository()
        self.processor = EventProcessor(
            data_dir=data_dir,
            repository=self.repository,
        )

    def test_process_payload_adds_derived_fields(self) -> None:
        payload = {
            "event_id": "11111111-1111-4111-8111-111111111111",
            "timestamp": "2026-04-06T10:00:00Z",
            "bus_id": "BUS_510_01",
            "line_id": "LINE_510",
            "route_direction": "outbound",
            "lat": 39.9212,
            "lon": 32.8538,
            "speed_kmh": 24.0,
            "next_stop_id": "STOP_SIH_02",
            "next_stop_name": "Sihhiye Koprusu",
            "boarding_count": 3,
        }

        enriched = self.processor.process_payload(payload)

        self.assertIn("estimated_eta_sec", enriched)
        self.assertIn("estimated_alighting_count", enriched)
        self.assertIn("estimated_occupancy_score", enriched)
        self.assertIn("estimated_occupancy_level", enriched)
        self.assertIn("is_delayed", enriched)
        self.assertGreaterEqual(enriched["estimated_eta_sec"], 20)
        self.assertIn(enriched["estimated_occupancy_level"], {"dusuk", "orta", "yuksek"})
        self.assertEqual(len(self.repository.history), 1)
        self.assertEqual(self.repository.history[0]["bus_id"], "BUS_510_01")

    def test_lambda_handler_accepts_kinesis_envelope(self) -> None:
        payload = {
            "event_id": "22222222-2222-4222-8222-222222222222",
            "timestamp": "2026-04-06T10:00:00Z",
            "bus_id": "BUS_520_01",
            "line_id": "LINE_520",
            "route_direction": "outbound",
            "lat": 39.9415,
            "lon": 32.8546,
            "speed_kmh": 20.0,
            "next_stop_id": "STOP_OPR_09",
            "next_stop_name": "Opera",
            "boarding_count": 2,
        }
        encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        event = {
            "Records": [
                {
                    "kinesis": {
                        "data": encoded,
                    }
                }
            ]
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["processed_count"], 1)
        self.assertEqual(result["records"][0]["bus_id"], "BUS_520_01")

    def test_invalid_payload_raises(self) -> None:
        invalid_payload = {
            "event_id": "33333333-3333-4333-8333-333333333333",
            "timestamp": "2026-04-06T10:00:00Z",
            "bus_id": "BUS_530_01",
        }

        with self.assertRaises(ValueError):
            self.processor.process_payload(invalid_payload)


if __name__ == "__main__":
    unittest.main()
