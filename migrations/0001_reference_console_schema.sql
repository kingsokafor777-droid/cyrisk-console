-- PostgreSQL reference migration only. This repository does not connect to or apply it.
-- A deployer must authenticate identities, set tenant context safely, restrict privileges, and
-- validate RLS policy behavior in its own runtime before using any analogous schema.

CREATE TABLE cyrisk_console_record_reference (
    tenant_id TEXT NOT NULL,
    record_id TEXT NOT NULL,
    record_kind TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    integrity_hash CHAR(64) NOT NULL,
    metadata_json JSONB NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (tenant_id, record_id)
);

ALTER TABLE cyrisk_console_record_reference ENABLE ROW LEVEL SECURITY;

-- Intentionally no permissive RLS policy is supplied. The deployer owns a least-privilege policy
-- tied to authenticated tenant context; enabling RLS alone does not provide an authorization design.
