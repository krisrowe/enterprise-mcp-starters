import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {
  QueryFilterSchema,
  toolGetServerTime,
  toolInspectCallerIdentity,
  toolQuerySampleRecords,
} from "./tools";
import { extractCallerContext } from "./auth";

export function createMCPServer() {
  const server = new Server(
    {
      name: "enterprise-mcp-starter-node",
      version: "0.1.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "get_server_time",
          description: "Retrieve the current server time in UTC ISO 8601 format.",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "inspect_caller_identity",
          description: "Inspect the authenticated caller identity and scopes.",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "query_sample_records",
          description: "Query sample enterprise records with optional category filtering.",
          inputSchema: {
            type: "object",
            properties: {
              category: {
                type: "string",
                description: "Optional category filter (finance, engineering, ops)",
              },
              limit: {
                type: "integer",
                description: "Maximum records to return (default: 5)",
                default: 5,
              },
            },
          },
        },
      ],
    };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    if (name === "get_server_time") {
      return {
        content: [{ type: "text", text: JSON.stringify(toolGetServerTime(), null, 2) }],
      };
    }

    if (name === "inspect_caller_identity") {
      const ctx = extractCallerContext({}, "stdio");
      return {
        content: [{ type: "text", text: JSON.stringify(toolInspectCallerIdentity(ctx), null, 2) }],
      };
    }

    if (name === "query_sample_records") {
      const parsed = QueryFilterSchema.parse(args || {});
      return {
        content: [{ type: "text", text: JSON.stringify(toolQuerySampleRecords(parsed), null, 2) }],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  });

  return server;
}
