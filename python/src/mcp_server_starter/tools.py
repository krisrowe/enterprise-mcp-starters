"""Domain Tools Implementation.

Replace the sample tools in this file with your enterprise domain logic.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .auth import CallerContext


class QueryFilter(BaseModel):
    category: Optional[str] = Field(None, description="Optional category filter (e.g. 'finance', 'engineering', 'ops')")
    limit: int = Field(default=5, ge=1, le=50, description="Maximum number of records to return")


# Sample in-memory enterprise records
SAMPLE_DATABASE = [
    {"id": "REC-001", "name": "Global Inventory Feed", "category": "ops", "status": "active"},
    {"id": "REC-002", "name": "Quarterly Billing Pipeline", "category": "finance", "status": "active"},
    {"id": "REC-003", "name": "Observability Ingestion Gateway", "category": "engineering", "status": "active"},
    {"id": "REC-004", "name": "Fleet Dispatch Ledger", "category": "ops", "status": "maintenance"},
    {"id": "REC-005", "name": "Core Identity Provider Sync", "category": "engineering", "status": "active"},
]


def tool_get_server_time() -> Dict[str, str]:
    """Returns the current server time in UTC ISO 8601 format."""
    return {
        "status": "ok",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "service": "enterprise-mcp-starter"
    }


def tool_inspect_caller_identity(context: CallerContext) -> Dict[str, Any]:
    """Inspects the authenticated caller identity and scopes granted by the gateway."""
    return {
        "identity": context.identity,
        "client_id": context.client_id,
        "scopes": context.scopes,
        "is_authenticated": context.is_authenticated,
        "mode": "authorized" if context.is_authenticated else "unauthenticated"
    }


def tool_query_sample_records(filter_params: QueryFilter, context: Optional[CallerContext] = None) -> Dict[str, Any]:
    """Queries sample records with optional category filtering."""
    results = SAMPLE_DATABASE
    if filter_params.category:
        cat_lower = filter_params.category.lower()
        results = [r for r in results if r["category"] == cat_lower]

    limited = results[:filter_params.limit]
    return {
        "count": len(limited),
        "total_available": len(results),
        "records": limited
    }
