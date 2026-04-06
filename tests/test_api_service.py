from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from api.config import ApiSettings
from api.repository import JsonlReadRepository
from api.services import QueryService


class ApiServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_file = Path(self.temp_dir.name) / "enriched.jsonl"
        sample_events = [
            {
                "event_id": "a",
                "timestamp": "2026-04-06T10:00:00Z",
                "bus_id": "BUS_510_01",
                "line_id": "LINE_510",
                "route_direction": "outbound",
                "lat": 39.92,
                "lon": 32.85,
                "speed_kmh": 20.0,
                "next_stop_id": "STOP_SIH_02",
                "next_stop_name": "Sihhiye Koprusu",
                "boarding_count": 2,
                "estimated_eta_sec": 100,
                "estimated_alighting_count": 0,
                "estimated_occupancy_score": 12,
                "estimated_occupancy_level": "dusuk",
                "is_delayed": False,
            },
            {
                "event_id": "b",
                "timestamp": "2026-04-06T10:00:03Z",
                "bus_id": "BUS_510_01",
                "line_id": "LINE_510",
                "route_direction": "outbound",
                "lat": 39.921,
                "lon": 32.851,
                "speed_kmh": 22.0,
                "next_stop_id": "STOP_SIH_02",
                "next_stop_name": "Sihhiye Koprusu",
                "boarding_count": 0,
                "estimated_eta_sec": 90,
                "estimated_alighting_count": 1,
                "estimated_occupancy_score": 11,
                "estimated_occupancy_level": "dusuk",
                "is_delayed": False,
            },
            {
                "event_id": "c",
                "timestamp": "2026-04-06T10:00:03Z",
                "bus_id": "BUS_520_01",
                "line_id": "LINE_520",
                "route_direction": "inbound",
                "lat": 39.941,
                "lon": 32.854,
                "speed_kmh": 18.0,
                "next_stop_id": "STOP_OPR_09",
                "next_stop_name": "Opera",
                "boarding_count": 1,
                "estimated_eta_sec": 120,
                "estimated_alighting_count": 0,
                "estimated_occupancy_score": 30,
                "estimated_occupancy_level": "orta",
                "is_delayed": True,
            },
        ]
        self.source_file.write_text(
            "\n".join(json.dumps(item) for item in sample_events),
            encoding="utf-8",
        )
        settings = ApiSettings(
            storage_mode="jsonl",
            aws_region=None,
            dynamodb_endpoint_url=None,
            current_state_table_name="bus_current_state",
            enriched_events_file=self.source_file,
        )
        repository = JsonlReadRepository(self.source_file)
        self.service = QueryService(settings=settings, repository=repository)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_list_buses_returns_latest_state_per_bus(self) -> None:
        buses = self.service.list_buses()
        self.assertEqual(len(buses), 2)
        self.assertEqual(buses[0]["line_name"], "Kizilay - Sogutozu")

    def test_summary_aggregates_current_view(self) -> None:
        summary = self.service.get_summary()
        self.assertEqual(summary["total_buses"], 2)
        self.assertEqual(summary["delayed_bus_count"], 1)
        self.assertEqual(summary["occupancy_medium_count"], 1)

    def test_line_summaries_include_all_lines(self) -> None:
        lines = self.service.list_lines()
        line_ids = {item["line_id"] for item in lines}
        self.assertEqual(line_ids, {"LINE_510", "LINE_520", "LINE_530"})


if __name__ == "__main__":
    unittest.main()
