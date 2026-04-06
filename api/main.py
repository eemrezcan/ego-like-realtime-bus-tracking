from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .config import ApiSettings, load_api_settings
from .repository import ReadRepository, build_read_repository
from .schemas import (
    BusStateResponse,
    HealthResponse,
    LineSummaryResponse,
    SystemSummaryResponse,
)
from .services import QueryService


def create_app(
    settings: ApiSettings | None = None,
    repository: ReadRepository | None = None,
) -> FastAPI:
    resolved_settings = settings or load_api_settings()
    resolved_repository = repository or build_read_repository(resolved_settings)
    query_service = QueryService(
        settings=resolved_settings,
        repository=resolved_repository,
    )

    app = FastAPI(
        title="EGO Benzeri Otobus Takip API",
        version="0.1.0",
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> dict[str, object]:
        return query_service.get_health()

    @app.get("/buses", response_model=list[BusStateResponse])
    def list_buses() -> list[dict[str, object]]:
        return query_service.list_buses()

    @app.get("/buses/{bus_id}", response_model=BusStateResponse)
    def get_bus(bus_id: str) -> dict[str, object]:
        bus = query_service.get_bus(bus_id)
        if bus is None:
            raise HTTPException(status_code=404, detail="Bus not found")
        return bus

    @app.get("/lines", response_model=list[LineSummaryResponse])
    def list_lines() -> list[dict[str, object]]:
        return query_service.list_lines()

    @app.get("/summary", response_model=SystemSummaryResponse)
    def summary() -> dict[str, object]:
        return query_service.get_summary()

    return app


app = create_app()

