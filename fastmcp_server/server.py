from fastmcp import FastMCP
from fastapi import FastAPI, Body
import uvicorn

from fastmcp_server.parser import parse_log

# ---- MCP server setup ----
mcp = FastMCP("MCP Log Parser Server")

@mcp.tool()
def parse_log_tool(file_path: str) -> dict:
    return parse_log(file_path)


# ---- REST server setup ----
app = FastAPI(title="Mini QA Triage Helper API")

@app.post("/parse_log")
def parse_log_rest(file_path: str = Body(..., embed=True)):
    """
    Simple REST endpoint for testing.
    Example curl:
    curl -X POST http://localhost:8000/parse_log \
         -H "Content-Type: application/json" \
         -d '{"file_path": "./logs/sample.log"}'
    """
    return parse_log(file_path)


# ---- Run both (MCP + REST) ----
if __name__ == "__main__":
    import threading

    # Run FastMCP in a background thread
    def run_mcp():
        mcp.run(transport="http", host="localhost", port=8000)

    mcp_thread = threading.Thread(target=run_mcp, daemon=True)
    mcp_thread.start()

    # Run FastAPI (REST) normally — uses its own loop
    uvicorn.run(app, host="localhost", port=8080)



