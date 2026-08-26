# Architecture

The v0.1.0 application factory creates a read-only FastAPI service. A dependency reads a supplied
`X-Cyrisk-Tenant` and `X-Cyrisk-Role` header, validates allowed role/tenant values, and allows only
the fixed synthetic tenant. The service returns strict metadata response models from sealed fixture
records. There are no write routes and no external connections.

| Request condition | Result |
|---|---|
| Valid synthetic tenant and permitted role | Read-only synthetic workbench metadata. |
| Missing/unknown tenant, malformed role, or role outside the endpoint policy | `403` or `422`; no record is returned. |
| Attempted mutation route | No route exists in v0.1.0. |

The migration file documents a deployer-owned PostgreSQL shape. It is neither connected nor applied
by this repository. Its comments identify tenant filtering and database row-level security as
production responsibilities, not guarantees made by the local application.
