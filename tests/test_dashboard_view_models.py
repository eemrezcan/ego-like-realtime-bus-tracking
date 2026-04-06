from __future__ import annotations

import unittest

from dashboard.view_models import (
    build_bus_table_rows,
    build_map_dataframe,
    filter_buses_by_line,
    summarize_delay_label,
)


class DashboardViewModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.buses = [
            {
                "bus_id": "BUS_510_01",
                "line_id": "LINE_510",
                "line_name": "Kizilay - Sogutozu",
                "route_direction": "outbound",
                "timestamp": "2026-04-06T10:00:00Z",
                "lat": 39.92,
                "lon": 32.85,
                "speed_kmh": 21.5,
                "next_stop_id": "STOP_SIH_02",
                "next_stop_name": "Sihhiye Koprusu",
                "boarding_count": 2,
                "estimated_eta_sec": 95,
                "estimated_alighting_count": 1,
                "estimated_occupancy_score": 10,
                "estimated_occupancy_level": "dusuk",
                "is_delayed": False,
            },
            {
                "bus_id": "BUS_520_01",
                "line_id": "LINE_520",
                "line_name": "Ulus - Dikimevi",
                "route_direction": "inbound",
                "timestamp": "2026-04-06T10:00:00Z",
                "lat": 39.94,
                "lon": 32.86,
                "speed_kmh": 17.0,
                "next_stop_id": "STOP_OPR_09",
                "next_stop_name": "Opera",
                "boarding_count": 1,
                "estimated_eta_sec": 120,
                "estimated_alighting_count": 0,
                "estimated_occupancy_score": 28,
                "estimated_occupancy_level": "orta",
                "is_delayed": True,
            },
        ]

    def test_build_bus_table_rows_shapes_display_data(self) -> None:
        rows = build_bus_table_rows(self.buses)
        self.assertEqual(rows[0]["Bus"], "BUS_510_01")
        self.assertEqual(rows[1]["Doluluk"], "orta")

    def test_build_map_dataframe_returns_expected_columns(self) -> None:
        frame = build_map_dataframe(self.buses)
        self.assertEqual(len(frame), 2)
        self.assertIn("lat", frame.columns)
        self.assertIn("color_hex", frame.columns)

    def test_filter_buses_by_line_respects_selection(self) -> None:
        filtered = filter_buses_by_line(self.buses, "LINE_520")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["bus_id"], "BUS_520_01")

    def test_summarize_delay_label(self) -> None:
        self.assertEqual(summarize_delay_label(0), "Akis stabil")
        self.assertEqual(summarize_delay_label(2), "Hafif gecikme")
        self.assertEqual(summarize_delay_label(3), "Yogun gecikme")


if __name__ == "__main__":
    unittest.main()
