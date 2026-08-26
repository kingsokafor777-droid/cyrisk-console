"""FastAPI factory for the source-release console boundary."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from .auth import caller_context
from .models import (
    BoundaryResponse,
    CallerContext,
    ConsoleRole,
    ReviewContextResponse,
    WorkbenchResponse,
)
from .store import record_for_scenario, records_for_tenant

STATIC_INDEX = Path(__file__).parent / "static" / "index.html"
REVIEW_ROLES = frozenset({ConsoleRole.REVIEWER, ConsoleRole.ADMIN})
CallerContextDependency = Annotated[CallerContext, Depends(caller_context)]


def _require_review_role(context: CallerContext) -> CallerContext:
    if context.role not in REVIEW_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="review role required")
    return context


def create_app() -> FastAPI:
    """Create the local read-only API and static workbench reference application."""

    app = FastAPI(
        title="Cyrisk Console",
        version="0.1.0",
        description="Synthetic read-only reference boundary; not a deployed risk decision system.",
        docs_url="/docs",
        redoc_url=None,
    )

    @app.get("/", include_in_schema=False)
    def workbench() -> FileResponse:
        return FileResponse(STATIC_INDEX, media_type="text/html")

    @app.get("/api/v1/boundaries", response_model=BoundaryResponse)
    def boundaries() -> BoundaryResponse:
        return BoundaryResponse()

    @app.get("/api/v1/workbench", response_model=WorkbenchResponse)
    def workbench_records(context: CallerContextDependency) -> WorkbenchResponse:
        return WorkbenchResponse(
            tenant_id=context.tenant_id, records=records_for_tenant(context.tenant_id)
        )

    @app.get("/api/v1/workbench/{scenario_id}", response_model=WorkbenchResponse)
    def scenario_record(scenario_id: str, context: CallerContextDependency) -> WorkbenchResponse:
        record = record_for_scenario(context.tenant_id, scenario_id)
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scenario not found")
        return WorkbenchResponse(tenant_id=context.tenant_id, records=(record,))

    @app.get("/api/v1/review-context/{scenario_id}", response_model=ReviewContextResponse)
    def review_context(scenario_id: str, context: CallerContextDependency) -> ReviewContextResponse:
        context = _require_review_role(context)
        record = record_for_scenario(context.tenant_id, scenario_id)
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scenario not found")
        return ReviewContextResponse(
            tenant_id=context.tenant_id,
            scenario_id=record.scenario_id,
            risk_id=record.risk_id,
            review_status=record.review_status,
            observation_note="Fictional review metadata; no authority or decision is established.",
        )

    return app
