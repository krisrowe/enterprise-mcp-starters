# Enterprise MCP Server Starter (Python)

A production-ready, security-aware starter kit for building custom **Model Context Protocol (MCP)** servers in Python.

Powered by:
* **FastMCP** (official `mcp` SDK)
* **Starlette & Uvicorn** for HTTP streaming / SSE
* **Pydantic v2** for strict schema validation

---

## 60-Second Quickstart

### 1. Setup Environment
```bash
make setup
```
This hermetically creates a `.venv` and installs all dependencies and development tools.

### 2. Run Tests
```bash
make test
```

### 3. Run Locally (Choose Transport)

#### Option A: `stdio` mode (For Antigravity, Claude Code, Cursor)
```bash
python -m mcp_server_starter.server --transport stdio
```

#### Option B: `http` mode (For Web / API Gateway / Kubernetes)
```bash
python -m mcp_server_starter.server --transport http --port 8080
```
Verify the health check:
```bash
curl http://localhost:8080/healthz
# {"status":"healthy","service":"mcp-server"}
```

---

## Where Do I Put My Real Tools?

Open [`src/mcp_server_starter/tools.py`](src/mcp_server_starter/tools.py).

Replace the sample functions (`tool_get_server_time`, `tool_query_sample_records`) with your actual domain logic and Pydantic schemas. Tool schemas and documentation are automatically generated from Python type hints and docstrings.

---

## In-Depth Documentation

* 📖 [Local Development & MCP Inspector Guide](docs/local-development.md)
* 🛠️ [Adding and Securing Custom Tools](docs/adding-tools.md)
* 🔐 [Identity, Scopes, and Gateway Auth Patterns](docs/authentication.md)
* 🚢 [Containerization and Kubernetes Deployment](docs/enterprise-hosting.md)

---

## License

Apache 2.0.
