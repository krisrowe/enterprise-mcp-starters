# Local Development & Testing

## 1. Testing with the MCP Inspector

The official MCP Inspector provides an interactive web UI to test tool discovery and tool calls:

```bash
# In stdio mode:
npx @modelcontextprotocol/inspector python -m mcp_server_starter.server --transport stdio
```

Open `http://localhost:5173` in your browser. You can click **List Tools**, view JSON schemas, and execute tools directly.

---

## 2. Desktop & CLI AI Integration

### Antigravity & Cursor
Configure `stdio` transport pointing to the virtualenv python executable.

### Claude Code
Add the MCP server to Claude Code using `claude mcp add`:
```bash
claude mcp add my-enterprise-server -- /path/to/enterprise-mcp-starters/python/.venv/bin/python -m mcp_server_starter.server --transport stdio
```

---

## 3. Running Sociable Unit Tests

```bash
make test
```
All unit tests in `tests/test_server.py` run against real tool handlers without external mocks.
