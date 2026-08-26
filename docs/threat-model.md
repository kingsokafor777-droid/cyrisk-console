# Threat Model

| Threat | Example | Mitigation and boundary |
|---|---|---|
| Header impersonation | A caller provides another tenant header. | v0.1.0 is a local demonstration only; no production auth claim. |
| Cross-tenant record exposure | Query returns a different tenant’s records. | Fixed fixture tenancy and fail-closed tenant comparison tests. |
| Unauthorized state change | Console approves a decision or edits a record. | No write routes or mutation controls are implemented. |
| Data overclaim | Synthetic range metadata is portrayed as real loss. | Synthetic fixtures and visible limitations in all API/UI text. |
| Deployment overclaim | SQL reference is described as a running database. | No DB driver, connection URL, migration runner, or hosted endpoint. |
