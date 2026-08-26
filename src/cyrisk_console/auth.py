"""Demonstrative caller-context parser; not a production identity implementation."""

from __future__ import annotations

from fastapi import Header, HTTPException, status
from pydantic import ValidationError

from .models import TENANT_ID, CallerContext, ConsoleRole


def caller_context(
    x_cyrisk_tenant: str | None = Header(default=None),
    x_cyrisk_role: str | None = Header(default=None),
) -> CallerContext:
    """Require explicit synthetic tenant/role headers and reject unknown context fail-closed."""

    if x_cyrisk_tenant is None or x_cyrisk_role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="caller context required")
    try:
        context = CallerContext(tenant_id=x_cyrisk_tenant, role=ConsoleRole(x_cyrisk_role))
    except (ValidationError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="invalid context"
        ) from error
    if context.tenant_id != TENANT_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="tenant not available")
    return context
