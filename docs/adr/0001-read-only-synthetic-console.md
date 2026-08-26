# ADR 0001: Start with a read-only synthetic console boundary

**Status:** Accepted

The first console release is intentionally an API/UI reference rather than a deployed system. It
uses strict caller-context parsing to demonstrate where a real authorization dependency belongs,
but it does not authenticate identities or connect to PostgreSQL. This prevents a portfolio source
release from implying operational authorization, persistence, live risk processing, or workflow
authority that it does not provide.
