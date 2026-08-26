# Cyrisk Console

> **A source-release FastAPI boundary and static workbench shell for supplied, synthetic Cyrisk records—not a live product, deployment, identity provider, database, authorization service, risk engine, or decision workflow.**

`cyrisk-console` demonstrates a narrow read-only console contract. Its API exposes synthetic
tenant-scoped scenario, model, control-comparison, and risk-register metadata only after an explicit
caller-context check. The static workbench explains the boundaries of these fictional records.

| Surface | Included reference | Deliberate limitation |
|---|---|---|
| API | FastAPI read endpoints, strict response models, and caller-context role gate. | Header context is a local demonstration, not identity authentication. |
| Data | Sealed synthetic in-memory records and a PostgreSQL migration reference. | No database driver, migration execution, persistence, or customer data. |
| Workbench | Packaged static HTML showing review context and boundaries. | No live data fetch, mutation, approval, or remediation action. |
| RBAC | `analyst`, `reviewer`, and `admin` read permissions for a synthetic tenant. | Deployers must supply real identity, session, tenant membership, and authorization validation. |

The release pins [`cyrisk-core` v0.1.0](https://github.com/kingsokafor777-droid/cyrisk-core/releases/tag/v0.1.0)
commit `4d68f385ef382a6420466dff0196244a2c915f1f`. It is intentionally source-release
focused: no hosted URL, database, cloud account, live evidence, financial estimate, risk acceptance,
or compliance claim is implied.
