# Release Governance

## Candidate: v0.1.0

| Item | Verified local value |
|---|---|
| Package | `cyrisk-console` v0.1.0 |
| Core compatibility pin | `cyrisk-core` commit `4d68f385ef382a6420466dff0196244a2c915f1f` |
| API schema | `cyrisk.console/v1` |
| Sealed synthetic API fixture SHA-256 | `6c6343a07ab0dfceeba1fc5574192de43ccba529ce1d2dcf116ba2dd3dac7a44` |
| Local behavioral result | `make check` passed: fixture reproducibility, Ruff, strict mypy, 11 tests, and 98.54% branch-aware coverage |
| Wheel SHA-256 | `ab0130d5ae896fca8af8fb81f39f0bc0191a5e54d9a9b3d1c77dc656d41d744f` |

Publication remains approval-gated. After explicit approval, the procedure must create the public
repository, tag the reviewed commit, attach the verified wheel, wait for successful hosted
`Quality`, Python 3.10–3.13, and `Analyze Python` checks, retrieve exact check contexts, apply the
protected-main policy, and synchronize the profile and program ledger.

The FastAPI source boundary demonstrates only fixed synthetic records and a caller-context parsing
location. It does not authenticate an identity, validate authorization, connect to PostgreSQL, apply
the migration reference, access cloud/evidence systems, calculate risk, approve/accept a decision,
verify remediation, or deploy a console. A successful CodeQL workflow must not be used to claim a
code-scanning-alert count without an accessible platform result.
