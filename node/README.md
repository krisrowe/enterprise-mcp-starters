# Enterprise MCP Server Starter (TypeScript / Node.js)

A production-ready, security-aware starter kit for building custom **Model Context Protocol (MCP)** servers in TypeScript / Node.js.

Powered by:
* **`@modelcontextprotocol/sdk`** (Official TypeScript SDK)
* **Express** for HTTP streaming / SSE and Kubernetes health endpoints
* **Zod** for strict parameter validation

---

## 60-Second Quickstart

### 1. Setup Environment
```bash
make setup
```

### 2. Run Tests
```bash
make test
```

### 3. Run Locally (Choose Transport)

#### Option A: `stdio` mode (For Antigravity, Claude Code, Cursor)
```bash
npm run dev:stdio
```

#### Option B: `http` mode (For Web / API Gateway / Kubernetes)
```bash
npm run dev
```

Verify the health check:
```bash
curl http://localhost:8080/healthz
# {"status":"healthy","service":"mcp-server-node"}
```

---

## Where Do I Put My Real Tools?

Open [`src/tools.ts`](src/tools.ts).

Replace the sample functions (`toolGetServerTime`, `toolQuerySampleRecords`) and schemas with your actual domain logic. Tool schemas in [`src/server.ts`](src/server.ts) are registered with standard MCP handlers.

---

## In-Depth Documentation

* 📖 [Local Development & MCP Inspector Guide](../python/docs/local-development.md)
* 🛠️ [Adding and Securing Custom Tools](../python/docs/adding-tools.md)
* 🔐 [Identity, Scopes, and Gateway Auth Patterns](../python/docs/authentication.md)
* 🚢 [Containerization and Kubernetes Deployment](../python/docs/enterprise-hosting.md)

---

## License

Apache 2.0.
