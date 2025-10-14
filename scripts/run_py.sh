#!/usr/bin/env bash
# ==========================
# Run Hugging Face MCP host
# ==========================

# Exit if any command fails
set -e

# --- Activate venv ---
if [[ -d ".venv" ]]; then
  source ".venv/bin/activate"
fi

# --- Start FastMCP server in background ---
echo "Starting FastMCP server on http://localhost:8000/mcp ..."
python -m fastmcp_server.server &
MCP_PID=$!

# --- Wait a few seconds to ensure the server starts ---
sleep 5

# --- Define cleanup to stop background process ---
cleanup() {
  echo "🛑 Stopping FastMCP server (PID: $MCP_PID)..."
  kill $MCP_PID 2>/dev/null || true
}
trap cleanup EXIT

# 3. Run the Hugging Face MCP host
# It uses config.json to connect to your local FastMCP server
echo "🤖 Starting Hugging Face MCP host ..."
tiny-agents run ./config.json
