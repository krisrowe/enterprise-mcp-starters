import { z } from "zod";
import { CallerContext } from "./auth";

export const QueryFilterSchema = z.object({
  category: z.string().optional().describe("Optional category filter (e.g. 'finance', 'engineering', 'ops')"),
  limit: z.number().int().min(1).max(50).default(5).describe("Maximum number of records to return")
});

export type QueryFilter = z.infer<typeof QueryFilterSchema>;

const SAMPLE_DATABASE = [
  { id: "REC-001", name: "Global Inventory Feed", category: "ops", status: "active" },
  { id: "REC-002", name: "Quarterly Billing Pipeline", category: "finance", status: "active" },
  { id: "REC-003", name: "Observability Ingestion Gateway", category: "engineering", status: "active" },
  { id: "REC-004", name: "Fleet Dispatch Ledger", category: "ops", status: "maintenance" },
  { id: "REC-005", name: "Core Identity Provider Sync", category: "engineering", status: "active" },
];

export function toolGetServerTime() {
  return {
    status: "ok",
    timestamp_utc: new Date().toISOString(),
    service: "enterprise-mcp-starter-node"
  };
}

export function toolInspectCallerIdentity(context: CallerContext) {
  return {
    identity: context.identity,
    client_id: context.clientId,
    scopes: context.scopes,
    is_authenticated: context.isAuthenticated,
    mode: context.isAuthenticated ? "authorized" : "unauthenticated"
  };
}

export function toolQuerySampleRecords(params: QueryFilter) {
  let results = SAMPLE_DATABASE;
  if (params.category) {
    const cat = params.category.toLowerCase();
    results = results.filter(r => r.category === cat);
  }

  const limited = results.slice(0, params.limit);
  return {
    count: limited.length,
    total_available: results.length,
    records: limited
  };
}
