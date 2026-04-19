from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - Optional outside local development.
    def load_dotenv(*_args: object, **_kwargs: object) -> bool:
        return False


@dataclass(frozen=True)
class DashboardSettings:
    api_base_url: str
    default_selected_line: str
    auto_refresh_seconds: int


def load_dashboard_settings() -> DashboardSettings:
    base_dir = Path(__file__).resolve().parents[1]
    load_dotenv(base_dir / ".env")

    api_base_url = os.getenv("DASHBOARD_API_BASE_URL", "http://127.0.0.1:8000").strip()
    default_selected_line = os.getenv("DASHBOARD_DEFAULT_LINE", "").strip()
    auto_refresh_seconds = _parse_auto_refresh_seconds(
        os.getenv("DASHBOARD_AUTO_REFRESH_SECONDS", "5")
    )

    return DashboardSettings(
        api_base_url=api_base_url.rstrip("/"),
        default_selected_line=default_selected_line,
        auto_refresh_seconds=auto_refresh_seconds,
    )


def _parse_auto_refresh_seconds(raw_value: str) -> int:
    try:
        seconds = int(raw_value.strip())
    except (TypeError, ValueError):
        return 5

    return max(0, seconds)
