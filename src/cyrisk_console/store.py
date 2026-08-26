"""Fixed fictional records; no database driver, storage, mutation, or external retrieval."""

from __future__ import annotations

from .models import TENANT_ID, SyntheticScenarioRecord

SYNTHETIC_RECORDS: tuple[SyntheticScenarioRecord, ...] = (
    SyntheticScenarioRecord(
        tenant_id=TENANT_ID,
        scenario_id="scenario_console",
        risk_id="risk_console",
        title="Fictional synthetic workbench scenario",
        asset_id="asset_console",
        unit="synthetic-index-units",
        model_run_hash="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        scenario_hash="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        review_status="reviewed",
        completeness_status="partial",
        limitation=(
            "Fictional metadata only; no risk, loss, decision, authority, or "
            "remediation conclusion may be inferred."
        ),
    ),
)


def records_for_tenant(tenant_id: str) -> tuple[SyntheticScenarioRecord, ...]:
    """Return fixed records only when the requested synthetic tenant matches exactly."""

    return tuple(record for record in SYNTHETIC_RECORDS if record.tenant_id == tenant_id)


def record_for_scenario(tenant_id: str, scenario_id: str) -> SyntheticScenarioRecord | None:
    """Return one synthetic record without cross-tenant fallback behavior."""

    return next(
        (record for record in records_for_tenant(tenant_id) if record.scenario_id == scenario_id),
        None,
    )
