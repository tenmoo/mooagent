# MCP Test Server

A simple MCP (Model Context Protocol) server for testing MooAgent's MCP integration.

## Features

This test server provides 4 example tools:

1. **calculator** - Perform basic math operations (add, subtract, multiply, divide)
2. **weather** - Get simulated weather data for cities
3. **time** - Get current time in any timezone
4. **uuid** - Generate random UUIDs

## Quick Start

### 1. Install Dependencies

```bash
cd test-mcp-server
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python mcp_test_server.py
```

You should see:
```
🚀 Starting MCP Test Server...
📍 Server will be available at: http://localhost:3001
🛠️  Available tools: calculator, weather, time, uuid
```

### 3. Configure MooAgent

Add to your `backend/.env`:
```env
MCP_SERVER_URL=http://localhost:3001
```

### 4. Restart MooAgent Backend

```bash
cd ../backend
python main.py
```

### 5. Test in Chat

Open http://localhost:3000 and try:

- "What's 25 plus 17?"
- "What's the weather in Tokyo?"
- "What time is it in London?"
- "Generate a UUID"
- Click "Show Tools" to see all available MCP tools

## API Endpoints

### List Tools
```bash
curl -X POST http://localhost:3001/tools/list \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

### Call Calculator
```bash
curl -X POST http://localhost:3001/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "calculator",
      "arguments": {
        "operation": "add",
        "a": 15,
        "b": 27
      }
    }
  }'
```

### Get Weather
```bash
curl -X POST http://localhost:3001/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "weather",
      "arguments": {
        "city": "Tokyo"
      }
    }
  }'
```

## Supported Cities (Weather)

- Tokyo
- London
- New York
- Paris
- Sydney
- Any other city (returns default data)

## Example Conversations

**Math:**
```
You: What's 42 multiplied by 3?
MooAgent: [Uses calculator tool] 42 multiply 3 = 126
```

**Weather:**
```
You: How's the weather in London?
MooAgent: [Uses weather tool] Weather in London: Cloudy, 12°C, Humidity: 80%
```

**Time:**
```
You: What time is it in Tokyo?
MooAgent: [Uses time tool] Current time in Tokyo: 2026-01-12 15:30:45 JST
```

## Extending the Server

Add new tools by:

1. Adding tool definition to `TOOLS` list
2. Creating a handler function like `handle_calculator()`
3. Adding the tool to the `call_tool()` function

Example:
```python
def handle_my_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    # Your tool logic here
    return {"result": "Tool output"}
```

## Troubleshooting

**Port already in use:**
```bash
# Change port in mcp_test_server.py
uvicorn.run(app, host="0.0.0.0", port=3002)  # Use different port
```

**MooAgent can't connect:**
- Check server is running: `curl http://localhost:3001`
- Verify `MCP_SERVER_URL` in backend `.env`
- Check CORS settings if accessing from different origin

## Production Use

This is a **test server** for development. For production:

- Add authentication
- Implement rate limiting
- Add proper error handling
- Use production-grade database
- Deploy to a proper hosting service
- Add monitoring and logging

## Resources

- **MCP Specification**: https://modelcontextprotocol.io
- **MooAgent Docs**: ../docs/MCP_INTEGRATION.md
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

Happy testing! 🎉
