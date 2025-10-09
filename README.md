# Mini QA Triage Helper

This is a prototype project that explores using the **Model Context Protocol (MCP)** 
to assist QA engineers in log triage. 

- Local FastMCP server will parse logs (last 200 lines, error patterns).
- Hugging Face MCP server (LLaMA 3.1) will analyze the parsed errors.
- MCP Host will coordinate the flow and return root causes with suggested QA steps.

## Logs

The `logs/` folder contains **sample log files** used for testing the Mini QA Triage Helper:

- **sample.log** – A larger log with mixed INFO, WARN, and several ERROR lines (SQLTimeout, NullPointer, ConnectException) to test full parsing and AI summarization.
- **sample_small.log** – A very small log (5–6 lines) with only one error for quick or demo runs.

These files are ignored by Git (see `.gitignore`) and exist only for local development and testing purposes.

## Planned Local FastMCP Tool
- Name: `parse_log(file_path)`
- Purpose: Extract last N lines and error patterns from a log file.
- Output: Structured JSON of error types and counts.

## Architecture
- `fastmcp_server/parser.py`: Parses log files into structured error summaries.
- `fastmcp_server/server.py`: Runs a local FastMCP-compatible service exposing `parse_log`.
- `config.json`: Configures the MCP host connection to the local FastMCP server (and optionally the Hugging Face MCP host).


## 🚀 How to Run the Mini QA Triage Helper

### 1️⃣ Start the Local FastMCP + REST Server

The project runs two layers:

- **MCP server** — exposes `parse_log_tool(file_path)` for LLM or host connections.  
- **REST server** — optional test endpoint at `http://localhost:8080/parse_log`.

```bash
#To start the MCP server:
python -m fastmcp_server.server


#Expected output:
🖥️  Server name: MCP Log Parser Server
📦 Transport:    Streamable-HTTP
🔗 Server URL:   http://localhost:8000/mcp
```

 ### 2️⃣ Test the REST Endpoint
```bash
   curl -X POST http://localhost:8080/parse_log \
  -H "Content-Type: application/json" \
  -d '{"file_path": "./logs/sample.log"}'
```  

```bash
#Expected response:
{
  "errors": [
    {"type": "java.sql.SQLTimeoutException", "count": 1, "examples": ["Timeout waiting for connection from pool"]},
    {"type": "com.retailapp.db.ConnectionManager", "count": 1, "examples": ["- Failed to connect to database"]}
  ]
}
```


## 📈 Current Status

- ✅ **FastMCP server** runs locally at `http://localhost:8000/mcp`, exposing `parse_log_tool(file_path)`.
- ✅ **REST endpoint** (`http://localhost:8080/parse_log`) works for quick testing via curl or Postman.
- ✅ **Log parser module** returns structured JSON summaries from sample logs.
- ⚙️ **Next step:** connect this local FastMCP server to the **Hugging Face MCP host** via `config.json` for AI-driven error analysis and triage recommendations.
- 📁 **Repo ready for extension** — includes virtual environment setup, config templates, and test data.

