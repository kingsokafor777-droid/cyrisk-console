from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from cyrisk_console import cli
from cyrisk_console.app import create_app
from cyrisk_console.auth import caller_context
from cyrisk_console.models import TENANT_ID, ConsoleRole
from cyrisk_console.store import record_for_scenario, records_for_tenant

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PATH = ROOT / "fixtures" / "expected_api.json"
ANALYST_HEADERS = {"X-Cyrisk-Tenant": TENANT_ID, "X-Cyrisk-Role": "analyst"}
REVIEWER_HEADERS = {"X-Cyrisk-Tenant": TENANT_ID, "X-Cyrisk-Role": "reviewer"}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_boundaries_are_explicit_and_no_write_capability_is_claimed(client: TestClient) -> None:
    response = client.get("/api/v1/boundaries")
    assert response.status_code == 200
    assert response.json() == json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))["boundaries"]
    assert client.post("/api/v1/workbench", headers=ANALYST_HEADERS).status_code == 405


def test_workbench_returns_only_the_expected_synthetic_tenant_record(client: TestClient) -> None:
    response = client.get("/api/v1/workbench", headers=ANALYST_HEADERS)
    assert response.status_code == 200
    assert response.json() == json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))["workbench"]
    assert response.json()["records"][0]["unit"] == "synthetic-index-units"


@pytest.mark.parametrize(
    ("headers", "status_code"),
    [
        ({}, 403),
        ({"X-Cyrisk-Tenant": TENANT_ID}, 403),
        ({"X-Cyrisk-Tenant": "other_tenant", "X-Cyrisk-Role": "analyst"}, 403),
        ({"X-Cyrisk-Tenant": TENANT_ID, "X-Cyrisk-Role": "unknown"}, 422),
    ],
)
def test_workbench_rejects_missing_unknown_or_malformed_context(
    client: TestClient, headers: dict[str, str], status_code: int
) -> None:
    assert client.get("/api/v1/workbench", headers=headers).status_code == status_code


def test_scenario_query_is_tenant_scoped_and_not_found_is_explicit(client: TestClient) -> None:
    known = client.get("/api/v1/workbench/scenario_console", headers=ANALYST_HEADERS)
    unknown = client.get("/api/v1/workbench/scenario_missing", headers=ANALYST_HEADERS)
    assert known.status_code == 200
    assert len(known.json()["records"]) == 1
    assert unknown.status_code == 404


def test_review_context_requires_reviewer_or_admin_role(client: TestClient) -> None:
    analyst = client.get("/api/v1/review-context/scenario_console", headers=ANALYST_HEADERS)
    reviewer = client.get("/api/v1/review-context/scenario_console", headers=REVIEWER_HEADERS)
    missing = client.get("/api/v1/review-context/scenario_missing", headers=REVIEWER_HEADERS)
    assert analyst.status_code == 403
    assert reviewer.status_code == 200
    assert reviewer.json()["review_status"] == "reviewed"
    assert "authority" in reviewer.json()["limitation"]
    assert missing.status_code == 404


def test_context_parser_and_store_helpers_fail_closed() -> None:
    context = caller_context(TENANT_ID, ConsoleRole.ADMIN.value)
    assert context.role is ConsoleRole.ADMIN
    assert len(records_for_tenant(TENANT_ID)) == 1
    assert records_for_tenant("other_tenant") == ()
    assert record_for_scenario(TENANT_ID, "scenario_console") is not None
    assert record_for_scenario("other_tenant", "scenario_console") is None


def test_static_workbench_is_packaged_and_discloses_boundaries(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Cyrisk Console" in response.text
    assert "does not fetch live data" in response.text
    assert "fetch(" not in response.text


def test_cli_hands_explicit_local_settings_to_uvicorn_without_starting_server(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, object] = {}

    def fake_run(application: str, **kwargs: object) -> None:
        observed["application"] = application
        observed.update(kwargs)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)
    assert cli.main(["--host", "127.0.0.2", "--port", "9090"]) == 0
    assert observed == {
        "application": "cyrisk_console.app:create_app",
        "host": "127.0.0.2",
        "port": 9090,
        "factory": True,
    }
