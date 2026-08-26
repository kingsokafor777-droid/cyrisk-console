"""Strict synthetic-console contracts with no persistence or decision semantics."""

from __future__ import annotations

from enum import Enum
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION: Final[Literal["cyrisk.console/v1"]] = "cyrisk.console/v1"
ID_PATTERN = r"^[a-z][a-z0-9_-]{2,63}$"
HASH_PATTERN = r"^[a-f0-9]{64}$"
TENANT_ID = "synthetic_tenant"


class StrictModel(BaseModel):
    """Fail closed on unknown fields at the API boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class ConsoleRole(str, Enum):
    ANALYST = "analyst"
    REVIEWER = "reviewer"
    ADMIN = "admin"


class CallerContext(StrictModel):
    """Demonstration context only; deployers must replace it with authenticated identity claims."""

    tenant_id: str = Field(pattern=ID_PATTERN)
    role: ConsoleRole


class SyntheticScenarioRecord(StrictModel):
    """Fictional, non-currency metadata for a supplied synthetic scenario view."""

    schema_version: Literal["cyrisk.console/v1"] = SCHEMA_VERSION
    tenant_id: str = Field(pattern=ID_PATTERN)
    scenario_id: str = Field(pattern=ID_PATTERN)
    risk_id: str = Field(pattern=ID_PATTERN)
    title: str = Field(min_length=1, max_length=160)
    asset_id: str = Field(pattern=ID_PATTERN)
    unit: Literal["synthetic-index-units"]
    model_run_hash: str = Field(pattern=HASH_PATTERN)
    scenario_hash: str = Field(pattern=HASH_PATTERN)
    review_status: Literal["draft", "reviewed", "recorded", "declined"]
    completeness_status: Literal["complete", "partial", "insufficient"]
    limitation: str = Field(min_length=1, max_length=500)


class WorkbenchResponse(StrictModel):
    """Tenant-scoped response with a non-decision limitation for every read view."""

    schema_version: Literal["cyrisk.console/v1"] = SCHEMA_VERSION
    tenant_id: str = Field(pattern=ID_PATTERN)
    records: tuple[SyntheticScenarioRecord, ...]
    limitation: str = (
        "Synthetic read view only; it does not authenticate identity, validate authority, "
        "calculate risk, accept risk, approve a decision, verify remediation, or connect "
        "to a live system."
    )


class ReviewContextResponse(StrictModel):
    """A supplied synthetic review-context view, never a decision or authority assertion."""

    schema_version: Literal["cyrisk.console/v1"] = SCHEMA_VERSION
    tenant_id: str = Field(pattern=ID_PATTERN)
    scenario_id: str = Field(pattern=ID_PATTERN)
    risk_id: str = Field(pattern=ID_PATTERN)
    review_status: Literal["draft", "reviewed", "recorded", "declined"]
    observation_note: str = Field(min_length=1, max_length=500)
    limitation: str = (
        "A supplied fictional review context only; reviewer authority and any risk decision remain "
        "outside this source release."
    )


class BoundaryResponse(StrictModel):
    """Machine-readable non-goals for console integrations and UI clients."""

    schema_version: Literal["cyrisk.console/v1"] = SCHEMA_VERSION
    write_routes_present: Literal[False] = False
    live_database_connected: Literal[False] = False
    identity_authenticated: Literal[False] = False
    risk_decision_capability: Literal[False] = False
