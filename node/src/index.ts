import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
import cors from "cors";
import { createMCPServer } from "./server";

const args = process.argv.slice(2);
const transportType = args.includes("--transport") ? args[args.indexOf("--transport") + 1] : "stdio";
const port = parseInt(process.env.PORT || "8080", 10);
const host = process.env.HOST || "0.0.0.0";

async function main() {
  const server = createMCPServer();

  if (transportType === "stdio") {
    const transport = new StdioServerTransport();
    await server.connect(transport);
  } else {
    const app = express();
    app.use(cors());

    // Kubernetes health endpoints
    app.get(["/healthz", "/readyz", "/health"], (req, res) => {
      res.json({ status: "healthy", service: "mcp-server-node" });
    });

    let sseTransport: SSEServerTransport | null = null;

    app.get("/sse", async (req, res) => {
      res.setHeader("X-Accel-Buffering", "no");
      sseTransport = new SSEServerTransport("/messages", res);
      await server.connect(sseTransport);
    });

    app.post("/messages", async (req, res) => {
      if (!sseTransport) {
        res.status(400).send("SSE connection not established");
        return;
      }
      await sseTransport.handlePostMessage(req, res);
    });

    app.listen(port, host, () => {
      console.log(`Enterprise MCP Server (Node) listening on http://${host}:${port}`);
    });
  }
}

main().catch((err) => {
  console.error("Fatal server error:", err);
  process.exit(1);
});
