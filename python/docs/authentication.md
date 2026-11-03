# Enterprise Identity & Authentication Patterns

Enterprise MCP servers deploy behind an API Gateway (Apigee, Envoy, Kong) that validates caller identity. This starter supports two primary architectures:

---

## Pattern A: Gateway-Brokered Identity (Recommended)

In this pattern, the API Gateway (e.g., Apigee Hybrid) validates the incoming OAuth / Okta token and verifies fine-grained authorization policies (e.g. OPA). 

Apigee then forwards the request southbound to the MCP container inside the private cluster overlay with trusted identity headers:

* `X-Remote-User`: The verified user or service principal (e.g., `app-user@example.com` or `nhi-agent-456`).
* `X-Caller-Scopes`: Authorized scopes (e.g., `records.read tool.query`).
* `X-Consumer-ID`: The unique client application identity.

### Safe Internal Gateway Rule
Inside the Kubernetes overlay, the MCP server only trusts these headers if traffic arrives through the gateway or mutual TLS (mTLS).

---

## Pattern B: Direct JWT Bearer Validation

If callers connect directly to the MCP server without an API gateway front-door:
1. Callers send `Authorization: Bearer <JWT>`.
2. Configure `JWKS_URI` and `ISSUER` in environment variables.
3. Replace the placeholder in `src/mcp_server_starter/auth.py` with direct token validation (using `PyJWT` or `cryptography`).

---

## Local Development Bypass

During local development with `stdio` (or when running tests with `AUTH_DISABLED=true`), authentication checks pass automatically, assigning developer identity so you can test tool functionality without mocking tokens.
