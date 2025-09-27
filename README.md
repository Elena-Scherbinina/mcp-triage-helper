# Mini QA Triage Helper

This is a prototype project that explores using the **Model Context Protocol (MCP)** 
to assist QA engineers in log triage. 

- Local FastMCP server will parse logs (last 200 lines, error patterns).
- Hugging Face MCP server (LLaMA 3.1) will analyze the parsed errors.
- MCP Host will coordinate the flow and return root causes with suggested QA steps.

## Current Status
Project setup with virtual environment, config placeholder, and sample logs.
