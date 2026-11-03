"""Enterprise Model Context Protocol (MCP) Server Entrypoint.

Supports:
- stdio transport: For local development with Antigravity, Claude Code, Cursor.
- http transport: Streamable HTTP / SSE listener behind an API Gateway / Ingress.
- /healthz and /readyz endpoints for Kubernetes probes.
"""

import argparse
import asyncio
import os
import sys
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

from .auth import CallerContext, extract_caller_context
from .tools import (
    QueryFilter,
    tool_get_server_time,
    tool_inspect_caller_identity,
    tool_query_sample_records,
)

# Initialize the FastMCP instance
mcp = FastMCP("enterprise-mcp-starter")


@mcp.tool()
def get_server_time() -> Dict[str, str]:
    """Retrieve the current server time in UTC ISO 8601 format."""
    return tool_get_server_time()


@mcp.tool()
def inspect_caller_identity() -> Dict[str, Any]:
    """Inspect the authenticated caller identity and scopes."""
    # Stdio mode inherits local developer identity
    ctx = extract_caller_context({}, transport="stdio")
    return tool_inspect_caller_identity(ctx)


@mcp.tool()
def query_sample_records(category: str = None, limit: int = 5) -> Dict[str, Any]:
    """Query sample enterprise records with optional category filtering."""
    params = QueryFilter(category=category, limit=limit)
    return tool_query_sample_records(params)


# --- Kubernetes Health Probes ---

async def healthz(request):
    """Liveness probe: verifies process is alive."""
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


async def readyz(request):
    """Readiness probe: verifies service is ready to accept traffic."""
    return JSONResponse({"status": "ready", "service": "mcp-server"})


def create_http_app():
    """Create the Starlette ASGI application with health routes and MCP SSE."""
    mcp_app = mcp.sse_app()
    
    app = Starlette(
        routes=[
            Route("/healthz", healthz),
            Route("/readyz", readyz),
            Route("/health", healthz),
        ]
    )
    # Mount the FastMCP SSE application
    app.mount("/", mcp_app)
    return app


def main():
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Enterprise MCP Server Starter")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type: stdio (default) or http"
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="HTTP bind host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8080")),
        help="HTTP bind port (default: 8080)"
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        print(f"Starting Enterprise MCP Server on http://{args.host}:{args.port}")
        app = create_http_app()
        uvicorn.run(app, host=args.host, port=args.port, proxy_headers=True, forwarded_allow_ips="*")


if __name__ == "__main__":
    main()
