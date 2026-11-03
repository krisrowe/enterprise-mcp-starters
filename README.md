# Enterprise MCP Server Starters

Production-ready, security-aware starter boilerplates for building and deploying custom **Model Context Protocol (MCP)** servers in enterprise environments.

This repository provides dual, fully self-contained starter templates supporting both enterprise languages:
* **[Python (`python/`)](python/README.md):** Powered by the official `mcp` SDK (`FastMCP` / Streamable HTTP) + Starlette / Uvicorn.
* **[TypeScript / Node.js (`node/`)](node/README.md):** Powered by `@modelcontextprotocol/sdk` + Express.

Both implementations are built for enterprise deployment behind API Gateways (e.g. Apigee, Envoy, Kong) and container platforms (Kubernetes / EKS / AKS / GKE / Cloud Run).

---

## Why These Frameworks Were Chosen

| Language | Framework Stack | Rationale |
| :--- | :--- | :--- |
| **Python** | **FastMCP** (official `mcp` SDK) + Starlette / Uvicorn | High-level decorator syntax (`@mcp.tool()`), automatic Pydantic schema generation, native async handlers, and built-in Streamable HTTP / SSE transport. |
| **Node.js** | **`@modelcontextprotocol/sdk`** + Express | Official TypeScript standard, Zod runtime parameter validation, standard SSE transport handling, and full type safety across tools. |

---

## Current Status & Verification

* **Python Starter:** Verified with automated unit tests (`pytest`). Supports `stdio` and `http` transports.
* **Node.js Starter:** Verified with automated unit tests (`jest`). Supports `stdio` and `http` transports.
* **Container Packaging:** Production multi-stage `Dockerfile` (non-root UID 10001/1000, Kubernetes Restricted Pod Security Standards) included in both projects, ready for CI/CD container builds.

---

## Key Enterprise Architectural Patterns

1. **Dual-Transport Flexibility:**
   * **Local `stdio`:** Zero-config local development with **Antigravity**, **Claude Code**, Cursor, or other MCP-compliant agents.
   * **Production `HTTP / SSE`:** Streamable HTTP service running in a container behind an enterprise ingress or API gateway.
2. **Dedicated Health Probes (`/healthz`, `/readyz`):**
   * Kubernetes liveness and readiness probes hit lightweight HTTP endpoints without tripping JSON-RPC routing errors.
3. **Enterprise Identity & Gateway Decoupling:**
   * Demonstrates both **Pattern A** (API Gateway terminates OAuth and forwards trusted headers like `X-Remote-User` and `X-Caller-Scopes`) and **Pattern B** (direct Bearer JWT validation).
   * Local `stdio` mode runs friction-free without JWT requirements.
4. **Hardened Multi-Stage Dockerfile:**
   * Minimal non-root container images compliant with Kubernetes Restricted Pod Security Standards.
5. **Strict JSON-RPC 2.0 Compliance:**
   * Proper JSON-RPC error mapping preventing internal server stack traces from leaking to calling AI agents.

---

## 60-Second Quickstart

### Python Quickstart
```bash
cd python
make setup
make test

# Run locally in stdio mode (Antigravity / Claude Code / Cursor):
python -m src.mcp_server_starter.server --transport stdio

# Run as an HTTP service:
python -m src.mcp_server_starter.server --transport http --port 8080
```
See the full [Python Documentation](python/README.md).

### TypeScript / Node.js Quickstart
```bash
cd node
make setup
make test

# Run locally in stdio mode (Antigravity / Claude Code / Cursor):
npm run dev:stdio

# Run as an HTTP service:
npm run dev
```
See the full [Node.js Documentation](node/README.md).

---

## Where Do I Put My Real Tools?

Both templates isolate tool definitions into a single, clean module:
* **Python:** Open [`python/src/mcp_server_starter/tools.py`](python/src/mcp_server_starter/tools.py). Replace the sample functions with your domain logic and Pydantic schemas.
* **Node.js:** Open [`node/src/tools.ts`](node/src/tools.ts). Replace the sample tool definitions with your domain logic and Zod schemas.

---

## Repository Structure

```
enterprise-mcp-starters/
├── README.md                 # This overview
├── Makefile                  # Root convenience targets
├── python/                   # Python MCP Starter
│   ├── README.md             # Python 60s quickstart
│   ├── Makefile              # Python setup, test, and run
│   ├── pyproject.toml        # Dependencies and packaging
│   ├── Dockerfile            # Hardened multi-stage container
│   ├── src/                  # Source code (server, auth, tools)
│   ├── tests/                # Unit & integration tests
│   └── docs/                 # Deep-dive guides
└── node/                     # TypeScript / Node.js MCP Starter
    ├── README.md             # Node 60s quickstart
    ├── Makefile              # Node setup, test, and run
    ├── package.json          # Dependencies and scripts
    ├── tsconfig.json         # TypeScript configuration
    ├── Dockerfile            # Hardened multi-stage container
    ├── src/                  # Source code (server, auth, tools)
    ├── tests/                # Unit tests
    └── docs/                 # Deep-dive guides
```

---

## License

Apache 2.0. Reusable for public, private, and enterprise development.
