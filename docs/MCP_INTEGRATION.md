# MCP Integration Guide

## Overview

MooAgent supports the **Model Context Protocol (MCP)**, allowing it to connect to remote MCP servers and access external tools and resources. This enables your AI agent to interact with file systems, databases, APIs, and any other MCP-compatible service.

**✅ Fully Working Implementation**

The MCP integration includes:
- Async HTTP communication with thread-based execution
- Compatible with uvloop (used by uvicorn)
- Automatic tool discovery in the chat UI
- Test MCP server with 4 example tools
- Natural language tool invocation
- Proper text wrapping and overflow handling in responses

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI applications connect to external data sources and tools. It provides:

- **Tools**: Executable functions that the AI can call
- **Resources**: Data and content that the AI can read
- **Prompts**: Pre-defined prompt templates
- **JSON-RPC**: Standard communication protocol

## Configuration

### 1. Set MCP Server URL

Add to your `backend/.env` file:

```env
MCP_SERVER_URL=http://localhost:3001
```

Or for remote servers:

```env
MCP_SERVER_URL=https://your-mcp-server.com
```

### 2. Use the Test Server (Recommended for Learning)

MooAgent includes a ready-to-use test MCP server:

```bash
cd test-mcp-server
pip install -r requirements.txt
python mcp_test_server.py
```

This starts a server with 4 example tools on port 3001.

### 3. Restart Backend

```bash
cd backend
python main.py
```

You should see:
```
✅ MCP sub-agent initialized with server: http://localhost:3001
```

## Usage

Once configured, the agent automatically has access to MCP tools. Users can interact naturally:

### Viewing Available Tools

Click **"Show Tools"** button in the chat interface to see:
- All built-in agent tools
- All MCP tools from the configured server
- Tool descriptions and parameters
- MCP server URL

### Example Conversations

**File System Access:**
```
User: "List the files in the documents folder"
Agent: [Calls MCP file system tool]
```

**Database Query:**
```
User: "Query the users table for active users"
Agent: [Calls MCP database tool]
```

**API Integration:**
```
User: "Get the weather for Tokyo"
Agent: [Calls MCP weather API tool]
```

## MCP Server Implementation

The MCP sub-agent (`backend/mcp_agent.py`) implements:

### Supported Operations

1. **List Tools** - Discover available tools
   ```python
   await mcp_agent.list_tools()
   ```

2. **Call Tools** - Execute a specific tool
   ```python
   await mcp_agent.call_tool("weather", {"city": "Tokyo"})
   ```

3. **List Resources** - Discover available resources
   ```python
   await mcp_agent.get_resources()
   ```

4. **Read Resources** - Read specific resource content
   ```python
   await mcp_agent.read_resource("file:///path/to/file")
   ```

### Protocol Details

**Endpoint Format:**
- Tools: `POST {MCP_SERVER_URL}/tools/list`, `POST {MCP_SERVER_URL}/tools/call`
- Resources: `POST {MCP_SERVER_URL}/resources/list`, `POST {MCP_SERVER_URL}/resources/read`

**Request Format:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "arg1": "value1"
    }
  }
}
```

**Response Format:**
```json
{
  "result": {
    "content": "Tool execution result"
  }
}
```

## Creating MCP Servers

You can create your own MCP servers in any language. Here's a simple example:

### Python MCP Server

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ToolCall(BaseModel):
    method: str
    params: dict

@app.post("/tools/list")
async def list_tools():
    return {
        "tools": [
            {
                "name": "greet",
                "description": "Greet a person by name",
                "parameters": {
                    "name": {"type": "string", "description": "Person's name"}
                }
            }
        ]
    }

@app.post("/tools/call")
async def call_tool(request: ToolCall):
    if request.params.get("name") == "greet":
        name = request.params.get("arguments", {}).get("name", "World")
        return {"result": f"Hello, {name}!"}
    
    return {"error": "Unknown tool"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
```

Run it:
```bash
python mcp_server.py
```

### Node.js MCP Server

```javascript
const express = require('express');
const app = express();
app.use(express.json());

app.post('/tools/list', (req, res) => {
  res.json({
    tools: [
      {
        name: 'greet',
        description: 'Greet a person by name',
        parameters: {
          name: { type: 'string', description: "Person's name" }
        }
      }
    ]
  });
});

app.post('/tools/call', (req, res) => {
  const { params } = req.body;
  if (params.name === 'greet') {
    const name = params.arguments?.name || 'World';
    res.json({ result: `Hello, ${name}!` });
  } else {
    res.json({ error: 'Unknown tool' });
  }
});

app.listen(3001, () => {
  console.log('MCP server running on port 3001');
});
```

## Example MCP Servers

### File System Server

```python
import os
from pathlib import Path

@app.post("/tools/call")
async def call_tool(request: ToolCall):
    tool_name = request.params.get("name")
    args = request.params.get("arguments", {})
    
    if tool_name == "list_files":
        path = args.get("path", ".")
        files = os.listdir(path)
        return {"result": files}
    
    elif tool_name == "read_file":
        path = args.get("path")
        content = Path(path).read_text()
        return {"result": content}
    
    return {"error": "Unknown tool"}
```

### Database Server

```python
import sqlite3

@app.post("/tools/call")
async def call_tool(request: ToolCall):
    tool_name = request.params.get("name")
    args = request.params.get("arguments", {})
    
    if tool_name == "query":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(args.get("sql"))
        results = cursor.fetchall()
        conn.close()
        return {"result": results}
    
    return {"error": "Unknown tool"}
```

## Security Considerations

### Authentication

Add authentication to your MCP server:

```python
from fastapi import Header, HTTPException

async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Unauthorized")
    token = authorization.split(" ")[1]
    # Verify token...
    return token

@app.post("/tools/call")
async def call_tool(request: ToolCall, token: str = Depends(verify_token)):
    # Process authenticated request
    pass
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/tools/call")
@limiter.limit("10/minute")
async def call_tool(request: ToolCall):
    pass
```

### Input Validation

Always validate and sanitize inputs:

```python
from pydantic import BaseModel, validator

class ToolArguments(BaseModel):
    path: str
    
    @validator('path')
    def validate_path(cls, v):
        # Prevent path traversal
        if '..' in v or v.startswith('/'):
            raise ValueError('Invalid path')
        return v
```

## Troubleshooting

### MCP Server Not Responding

1. Check if MCP server is running:
   ```bash
   curl http://localhost:3001/tools/list
   ```

2. Verify MCP_SERVER_URL in `.env`

3. Check backend logs for connection errors

### Tool Not Found

1. Verify tool name matches exactly
2. Check tool listing from MCP server
3. Ensure tool is properly registered

### Timeout Errors

The default timeout is 30 seconds. For long-running operations:

```python
# In backend/mcp_agent.py
self.client = httpx.AsyncClient(timeout=60.0)  # Increase timeout
```

## Advanced Usage

### Multiple MCP Servers

To connect to multiple MCP servers, modify `backend/agent.py`:

```python
mcp_servers = [
    ("FileSystem", "http://localhost:3001"),
    ("Database", "http://localhost:3002"),
]

for name, url in mcp_servers:
    wrapper = MCPToolWrapper(url)
    tools.append(Tool(
        name=f"MCP_{name}",
        func=wrapper.call_mcp_tool,
        description=f"Access {name} via MCP"
    ))
```

### Custom Tool Parsing

Enhance the tool wrapper to better parse natural language:

```python
def call_mcp_tool(self, tool_query: str) -> str:
    # Use LLM to parse query into tool call
    parsing_llm = ChatGroq(model="openai/gpt-oss-20b")  # Fast Groq-hosted model
    result = parsing_llm.invoke(
        f"Parse this request into tool_name and arguments: {tool_query}"
    )
    # Extract tool_name and arguments
    # Call MCP server
    pass
```

## Resources

- **MCP Specification**: https://modelcontextprotocol.io
- **MCP GitHub**: https://github.com/modelcontextprotocol
- **Example MCP Servers**: https://github.com/modelcontextprotocol/servers

## Support

For MCP integration issues:
1. Check backend logs
2. Test MCP server independently
3. Verify protocol implementation
4. Review error messages in chat

---

**Next Steps:**
- Create your own MCP server
- Connect to existing MCP servers
- Extend agent capabilities with custom tools
