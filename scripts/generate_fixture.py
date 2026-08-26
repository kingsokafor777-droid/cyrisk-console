"""Deliberately generate expected synthetic API responses from the local app factory."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from cyrisk_console.app import create_app

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PATH = ROOT / "fixtures" / "expected_api.json"
HEADERS = {"X-Cyrisk-Tenant": "synthetic_tenant", "X-Cyrisk-Role": "analyst"}


def main() -> int:
    client = TestClient(create_app())
    payload = {
        "boundaries": client.get("/api/v1/boundaries").json(),
        "workbench": client.get("/api/v1/workbench", headers=HEADERS).json(),
    }
    EXPECTED_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
