from __future__ import annotations

from typing import Any

import pandas as pd


OCCUPANCY_COLORS = {
    "dusuk": "#2A9D8F",
    "orta": "#EDAe49",
    "yuksek": "#D1495B",
}

OCCUPANCY_RGB_COLORS = {
    "dusuk": [42, 157, 143, 220],
    "orta": [237, 174, 73, 220],
    "yuksek": [209, 73, 91, 220],
}


def build_bus_table_rows(buses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bus in buses:
        rows.append(
            {
                "Bus": bus["bus_id"],
                "Hat": bus["line_id"],
                "Hat Adi": bus["line_name"],
                "Yon": "Gidis" if bus["route_direction"] == "outbound" else "Donus",
                "Hiz (km/h)": float(bus["speed_kmh"]),
                "Sonraki Durak": bus["next_stop_name"],
                "ETA (sn)": int(bus["estimated_eta_sec"]),
                "Doluluk": bus["estimated_occupancy_level"],
                "Gecikme": "Var" if bus["is_delayed"] else "Yok",
            }
        )
    return rows


def build_map_dataframe(buses: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for bus in buses:
        occupancy_level = str(bus["estimated_occupancy_level"])
        rows.append(
            {
                "lat": float(bus["lat"]),
                "lon": float(bus["lon"]),
                "bus_id": bus["bus_id"],
                "line_id": bus["line_id"],
                "line_name": bus["line_name"],
                "next_stop_name": bus["next_stop_name"],
                "estimated_eta_sec": int(bus["estimated_eta_sec"]),
                "estimated_occupancy_level": occupancy_level,
                "color_hex": OCCUPANCY_COLORS.get(
                    occupancy_level,
                    "#3A86FF",
                ),
                "color_rgba": OCCUPANCY_RGB_COLORS.get(
                    occupancy_level,
                    [58, 134, 255, 220],
                ),
                "marker_radius": 80,
            }
        )
    return pd.DataFrame(rows)


def filter_buses_by_line(
    buses: list[dict[str, Any]],
    selected_line: str | None,
) -> list[dict[str, Any]]:
    if not selected_line or selected_line == "Tum Hatlar":
        return buses
    return [bus for bus in buses if bus["line_id"] == selected_line]


def summarize_delay_label(delayed_bus_count: int) -> str:
    if delayed_bus_count == 0:
        return "Akis stabil"
    if delayed_bus_count <= 2:
        return "Hafif gecikme"
    return "Yogun gecikme"
