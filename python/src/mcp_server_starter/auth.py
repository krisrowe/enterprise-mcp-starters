"""Enterprise Identity & Caller Context Middleware.

Supports:
1. Pattern A: Gateway-brokered identity headers (Apigee / Envoy / Kong)
   - X-Remote-User: Caller identity (email / subject)
   - X-Caller-Scopes: Space- or comma-separated scopes granted to caller
   - X-Consumer-ID: Unique client ID or application ID
2. Pattern B: Direct Bearer token validation (JWT)
3. Local development bypass (stdio mode or AUTH_DISABLED=true)
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CallerContext:
    """Authenticated caller identity and permissions."""
    identity: str = "anonymous"
    client_id: str = "unknown"
    scopes: List[str] = field(default_factory=list)
    is_authenticated: bool = False

    def has_scope(self, scope: str) -> bool:
        """Check if caller possesses a specific scope."""
        return scope in self.scopes or "admin" in self.scopes or "*" in self.scopes


def extract_caller_context(headers: dict, transport: str = "http") -> CallerContext:
    """Extract and validate caller identity from request headers."""
    # Stdio transport: local execution inherits developer's identity
    if transport == "stdio":
        local_user = os.getenv("USER", "local-developer")
        return CallerContext(
            identity=local_user,
            client_id="local-cli",
            scopes=["*"],
            is_authenticated=True
        )

    # Allow local auth bypass for container / curl testing when explicitly configured
    if os.getenv("AUTH_DISABLED", "false").lower() in ("true", "1", "yes"):
        return CallerContext(
            identity="dev-user",
            client_id="dev-client",
            scopes=["*"],
            is_authenticated=True
        )

    # Pattern A: Gateway-injected headers
    remote_user = headers.get("x-remote-user") or headers.get("x-forwarded-user")
    caller_scopes_raw = headers.get("x-caller-scopes") or headers.get("x-scope") or ""
    client_id = headers.get("x-consumer-id") or headers.get("x-client-id") or "unknown"

    scopes = [s.strip() for s in caller_scopes_raw.replace(",", " ").split() if s.strip()]

    if remote_user:
        return CallerContext(
            identity=remote_user,
            client_id=client_id,
            scopes=scopes,
            is_authenticated=True
        )

    # Pattern B: Authorization Bearer header
    auth_header = headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        token = auth_header[7:].strip()
        # In production with Pattern B, plug in JWT validation against JWKS here.
        # For this template, a non-empty bearer token marks the caller as authenticated.
        return CallerContext(
            identity=f"bearer-caller-{token[:8]}",
            client_id=client_id,
            scopes=scopes or ["default"],
            is_authenticated=True
        )

    return CallerContext(
        identity="anonymous",
        client_id="anonymous",
        scopes=[],
        is_authenticated=False
    )
