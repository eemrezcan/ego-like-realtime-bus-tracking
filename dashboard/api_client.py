from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


class DashboardApiError(RuntimeError):
    """Dashboard'un API katmanindan veri okuyamadigi durumlar."""


@dataclass
class DashboardApiClient:
    base_url: str
    timeout_seconds: float = 5.0

    def get_health(self) -> dict[str, Any]:
        return self._get_json("/health")

    def get_summary(self) -> dict[str, Any]:
        return self._get_json("/summary")

    def get_lines(self) -> list[dict[str, Any]]:
        payload = self._get_json("/lines")
        if not isinstance(payload, list):
            raise DashboardApiError("/lines yaniti liste degil.")
        return payload

    def get_buses(self) -> list[dict[str, Any]]:
        payload = self._get_json("/buses")
        if not isinstance(payload, list):
            raise DashboardApiError("/buses yaniti liste degil.")
        return payload

    def get_bus(self, bus_id: str) -> dict[str, Any]:
        payload = self._get_json(f"/buses/{bus_id}")
        if not isinstance(payload, dict):
            raise DashboardApiError(f"/buses/{bus_id} yaniti dict degil.")
        return payload

    def _get_json(self, path: str) -> Any:
        url = f"{self.base_url}{path}"
        try:
            response = requests.get(url, timeout=self.timeout_seconds)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise DashboardApiError(
                f"API istegi basarisiz oldu: {url}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise DashboardApiError(f"API JSON donmedi: {url}") from exc

