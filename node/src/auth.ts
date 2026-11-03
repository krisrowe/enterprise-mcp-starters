/**
 * Enterprise Identity & Caller Context Middleware (Node.js).
 */

export interface CallerContext {
  identity: string;
  clientId: string;
  scopes: string[];
  isAuthenticated: boolean;
}

export function extractCallerContext(headers: Record<string, string | string[] | undefined>, transport: "http" | "stdio" = "http"): CallerContext {
  if (transport === "stdio") {
    return {
      identity: process.env.USER || "local-developer",
      clientId: "local-cli",
      scopes: ["*"],
      isAuthenticated: true
    };
  }

  // Check auth bypass for local test containers
  if (process.env.AUTH_DISABLED?.toLowerCase() === "true") {
    return {
      identity: "dev-user",
      clientId: "dev-client",
      scopes: ["*"],
      isAuthenticated: true
    };
  }

  // Pattern A: Gateway-injected headers
  const remoteUser = (headers["x-remote-user"] || headers["x-forwarded-user"]) as string | undefined;
  const rawScopes = (headers["x-caller-scopes"] || headers["x-scope"] || "") as string;
  const clientId = (headers["x-consumer-id"] || headers["x-client-id"] || "unknown") as string;

  const scopes = rawScopes.replace(/,/g, " ").split(/\s+/).filter(Boolean);

  if (remoteUser) {
    return {
      identity: remoteUser,
      clientId,
      scopes,
      isAuthenticated: true
    };
  }

  // Pattern B: Authorization Bearer
  const authHeader = (headers["authorization"] || "") as string;
  if (authHeader.toLowerCase().startsWith("bearer ")) {
    const token = authHeader.substring(7).trim();
    return {
      identity: `bearer-caller-${token.substring(0, 8)}`,
      clientId,
      scopes: scopes.length > 0 ? scopes : ["default"],
      isAuthenticated: true
    };
  }

  return {
    identity: "anonymous",
    clientId: "anonymous",
    scopes: [],
    isAuthenticated: false
  };
}

export function hasScope(ctx: CallerContext, scope: string): boolean {
  return ctx.scopes.includes(scope) || ctx.scopes.includes("admin") || ctx.scopes.includes("*");
}
