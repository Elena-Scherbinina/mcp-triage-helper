import httpx, json, asyncio

async def main():
    url = "http://localhost:8000/mcp"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    start_session = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "session/start",
        "params": {"sessionId": "test-session"}
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, content=json.dumps(start_session))
        print("🔹 Start session:", r.status_code)
        print(r.text)

asyncio.run(main())

