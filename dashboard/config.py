from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class DashboardSettings:
    api_base_url: str
    default_selected_line: str


def load_dashboard_settings() -> DashboardSettings:
    base_dir = Path(__file__).resolve().parents[1]
    load_dotenv(base_dir / ".env")

    api_base_url = os.getenv("DASHBOARD_API_BASE_URL", "http://127.0.0.1:8000").strip()
    default_selected_line = os.getenv("DASHBOARD_DEFAULT_LINE", "").strip()

    return DashboardSettings(
        api_base_url=api_base_url.rstrip("/"),
        default_selected_line=default_selected_line,
    )

