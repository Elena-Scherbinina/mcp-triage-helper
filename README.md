# 🧩 Mini QA Triage Helper

This is a prototype project that explores using the **Model Context Protocol (MCP)** 
to assist QA engineers in log triage. 

- Local FastMCP server will parse logs (last 200 lines, error patterns).
- Hugging Face MCP server (LLaMA 3.1) will analyze the parsed errors.
- MCP Host will coordinate the flow and return root causes with suggested QA steps.


## 📦 Installation

Clone the repository and set up the environment:
```bash
# Clone the project
git clone https://github.com/Elena-Scherbinina/mcp-triage-helper.git
cd mcp-triage-helper

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # (Mac/Linux)
# or on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# If not using requirements.txt, install manually:
pip install fastmcp "huggingface_hub[mcp]" uvicorn fastapi
```


```bash

## Quick Overview

| Feature     | Description                                      |
| ----------- | ------------------------------------------------ |
| 🧩 Protocol | Model Context Protocol (MCP)                     |
| ⚙️ Backend  | FastMCP (Python)                                 |
| 🧠 AI Layer | Hugging Face (LLaMA 3.1)                         |
| 🧾 Tool     | `parse_log(file_path)`                           |
| 🎯 Purpose  | Automate QA log triage and summarize root causes |



## 📁 Project Structure

mcp-triage-helper/
├── fastmcp_server/
│   ├── parser.py         ← Parses log files and extracts structured error data (types, counts, examples)
│   └── server.py         ← Runs both the FastMCP and REST servers (entry point for the backend)
│
├── logs/
│   ├── sample.log        ← Example log file with mixed INFO/WARN/ERROR messages for testing
│   └── sample_small.log  ← Smaller test log with a single error, used for quick verification
│
├── scripts/
│   └── run_py.sh         ← Shell script to start the Hugging Face MCP host and load config.json
│
├── config.json           ← Configuration file that connects your local FastMCP server to Hugging Face MCP
│
├── requirements.txt      ← Lists all Python dependencies (FastMCP, FastAPI, huggingface_hub, etc.)
│
├── .gitignore            ← Excludes local files (e.g., .env, venv, logs) from being committed to Git
│
└── README.md             ← Main project documentation (overview, setup, architecture, and usage)


```




## 🧾 Logs

The `logs/` folder contains **sample log files** used for testing the Mini QA Triage Helper:

- **sample.log** – A larger log with mixed INFO, WARN, and several ERROR lines (SQLTimeout, NullPointer, ConnectException) to test full parsing and AI summarization.
- **sample_small.log** – A very small log (5–6 lines) with only one error for quick or demo runs.

These files are ignored by Git (see `.gitignore`) and exist only for local development and testing purposes.


## ⚙️ Local FastMCP Tool
- Name: `parse_log(file_path)`
- Purpose: Extract last N lines and error patterns from a log file.
- Output: Structured JSON of error types and counts.


### 🧩 Architecture
- `fastmcp_server/parser.py`: Parses log files into structured error summaries.
- `fastmcp_server/server.py`: Runs a local FastMCP-compatible service exposing `parse_log`.
- `config.json`: Configures the MCP host connection to the local FastMCP server (and optionally the Hugging Face MCP host).


## 🚀 How to Run the Mini QA Triage Helper

### 🧠 Step 0 — Log in to Hugging Face
Before running the MCP host, make sure you’re authenticated with Hugging Face:

```bash
huggingface-cli login
```
You’ll be prompted to paste your Hugging Face access token (starts with hf_...).
The login is stored securely on your machine — you only need to do this once.


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

### 3️⃣ Run the Hugging Face MCP Host
After the FastMCP server is running, you can start the Hugging Face MCP host (the client agent) with:
```bash
bash scripts/run_py.sh

# Expected Output:
🤖 Starting Hugging Face MCP host ...
Agent loaded with 1 tools:
 • parse_log_tool
»
```
You can now interact with the host directly, for example:
```bash
Analyze errors in ./logs/sample.log and summarize what they mean.

```

### 💬 Example Output
```bash
# Prompt:
Analyze errors in ./logs/sample.log and summarize what they mean.

# Response:
Several connection and null-pointer issues detected:
• Timeout waiting for connection from pool
• Failed to connect to database
• NullPointerException in OrderService
• Connection refused to PaymentGateway

Suggested fixes:
• Review DB connection pool settings
• Check database reachability
• Fix null handling in OrderService
• Verify payment gateway connectivity
```


## 📊 Current Status

- ✅ **FastMCP server** runs locally at `http://localhost:8000/mcp`, exposing `parse_log_tool(file_path)`.
- ✅ **REST endpoint** (`http://localhost:8080/parse_log`) works for quick testing via curl or Postman.
- ✅ **Hugging Face MCP host** successfully connects to the local server via config.json.

- ✅ **Log parser module** returns structured JSON summaries from sample logs.

- ⚙️ **Next step:** extend the pipeline with model reasoning (LLaMA / Claude) for automatic root cause suggestions.

- 📁 **Repo ready for extension** — includes virtual environment setup, config templates, and test data.


## 🧭 Next Steps

- 🤝 Integrate LLaMA 3.1 or Claude for AI-based triage suggestions
- 🪄 Add a UI (Streamlit or Gradio) for interactive analysis
- 📦 Package as a reusable QA assistant tool

