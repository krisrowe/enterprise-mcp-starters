import { toolGetServerTime, toolInspectCallerIdentity, toolQuerySampleRecords } from "../src/tools";
import { extractCallerContext, hasScope } from "../src/auth";

describe("Enterprise MCP Server (Node) Unit Tests", () => {
  test("toolGetServerTime returns valid UTC timestamp", () => {
    const res = toolGetServerTime();
    expect(res.status).toBe("ok");
    expect(res.timestamp_utc).toBeDefined();
    expect(res.service).toBe("enterprise-mcp-starter-node");
  });

  test("extractCallerContext stdio inherits local user", () => {
    const ctx = extractCallerContext({}, "stdio");
    expect(ctx.isAuthenticated).toBe(true);
    expect(hasScope(ctx, "any.scope")).toBe(true);
  });

  test("extractCallerContext parses gateway headers", () => {
    const headers = {
      "x-remote-user": "developer@example.com",
      "x-caller-scopes": "records.read tools.execute",
      "x-consumer-id": "app-gateway-123"
    };
    const ctx = extractCallerContext(headers, "http");
    expect(ctx.isAuthenticated).toBe(true);
    expect(ctx.identity).toBe("developer@example.com");
    expect(ctx.clientId).toBe("app-gateway-123");
    expect(hasScope(ctx, "records.read")).toBe(true);
    expect(hasScope(ctx, "admin")).toBe(false);
  });

  test("toolQuerySampleRecords filters by category", () => {
    const res = toolQuerySampleRecords({ category: "finance", limit: 5 });
    expect(res.count).toBeGreaterThan(0);
    res.records.forEach((r) => {
      expect(r.category).toBe("finance");
    });
  });
});
