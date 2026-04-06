from __future__ import annotations

from pathlib import Path

from simulator.data_loader import load_catalog

from .config import ApiSettings
from .repository import ReadRepository


class QueryService:
    def __init__(
        self,
        settings: ApiSettings,
        repository: ReadRepository,
        data_dir: Path | None = None,
    ) -> None:
        base_dir = Path(__file__).resolve().parents[1]
        self.settings = settings
        self.repository = repository
        self.catalog = load_catalog(data_dir or (base_dir / "data"))

    def get_health(self) -> dict[str, object]:
        buses = self.repository.list_current_buses()
        return {
            "status": "ok",
            "storage_mode": self.settings.storage_mode,
            "current_bus_count": len(buses),
            "configured_line_count": len(self.catalog.lines),
            "configured_stop_count": len(self.catalog.stops),
        }

    def list_buses(self) -> list[dict[str, object]]:
        buses = self.repository.list_current_buses()
        enriched = [self._with_line_name(bus) for bus in buses]
        return sorted(enriched, key=lambda item: (str(item["line_id"]), str(item["bus_id"])))

    def get_bus(self, bus_id: str) -> dict[str, object] | None:
        item = self.repository.get_bus(bus_id)
        if item is None:
            return None
        return self._with_line_name(item)

    def list_lines(self) -> list[dict[str, object]]:
        buses = self.repository.list_current_buses()
        grouped: dict[str, list[dict[str, object]]] = {}
        for bus in buses:
            grouped.setdefault(str(bus["line_id"]), []).append(bus)

        summaries: list[dict[str, object]] = []
        for line_id, line in sorted(self.catalog.lines.items()):
            line_buses = grouped.get(line_id, [])
            summaries.append(
                {
                    "line_id": line_id,
                    "public_code": line.public_code,
                    "name": line.name,
                    "active_bus_count": len(line_buses),
                    "average_speed_kmh": _average_number(line_buses, "speed_kmh"),
                    "average_eta_sec": int(round(_average_number(line_buses, "estimated_eta_sec"))),
                    "delayed_bus_count": sum(1 for bus in line_buses if bool(bus["is_delayed"])),
                    "occupancy_low_count": sum(
                        1 for bus in line_buses if bus["estimated_occupancy_level"] == "dusuk"
                    ),
                    "occupancy_medium_count": sum(
                        1 for bus in line_buses if bus["estimated_occupancy_level"] == "orta"
                    ),
                    "occupancy_high_count": sum(
                        1 for bus in line_buses if bus["estimated_occupancy_level"] == "yuksek"
                    ),
                }
            )

        return summaries

    def get_summary(self) -> dict[str, object]:
        buses = self.repository.list_current_buses()
        latest_timestamp = max((str(bus["timestamp"]) for bus in buses), default=None)

        return {
            "total_buses": len(buses),
            "total_lines": len({str(bus["line_id"]) for bus in buses}),
            "delayed_bus_count": sum(1 for bus in buses if bool(bus["is_delayed"])),
            "average_speed_kmh": _average_number(buses, "speed_kmh"),
            "occupancy_low_count": sum(
                1 for bus in buses if bus["estimated_occupancy_level"] == "dusuk"
            ),
            "occupancy_medium_count": sum(
                1 for bus in buses if bus["estimated_occupancy_level"] == "orta"
            ),
            "occupancy_high_count": sum(
                1 for bus in buses if bus["estimated_occupancy_level"] == "yuksek"
            ),
            "latest_timestamp": latest_timestamp,
        }

    def _with_line_name(self, bus: dict[str, object]) -> dict[str, object]:
        line = self.catalog.lines[str(bus["line_id"])]
        return {
            **bus,
            "line_name": line.name,
        }


def _average_number(items: list[dict[str, object]], field_name: str) -> float:
    if not items:
        return 0.0
    total = sum(float(item[field_name]) for item in items)
    return round(total / len(items), 1)

