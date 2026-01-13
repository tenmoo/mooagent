"""
Simple MCP Test Server for MooAgent
A basic MCP server with example tools for testing
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

app = FastAPI(title="MCP Test Server", version="1.0.0")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRequest(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = {}


# Define example tools
TOOLS = [
    {
        "name": "calculator",
        "description": "Perform basic mathematical calculations",
        "parameters": {
            "operation": {
                "type": "string",
                "description": "The operation to perform",
                "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number",
                "description": "Second number"
            }
        }
    },
    {
        "name": "weather",
        "description": "Get weather information for a city (simulated data)",
        "parameters": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        }
    },
    {
        "name": "time",
        "description": "Get current time in a timezone",
        "parameters": {
            "timezone": {
                "type": "string",
                "description": "Timezone (e.g., UTC, America/New_York)",
                "default": "UTC"
            }
        }
    },
    {
        "name": "uuid",
        "description": "Generate a random UUID",
        "parameters": {}
    }
]


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "MCP Test Server",
        "version": "1.0.0",
        "description": "A simple MCP server for testing MooAgent",
        "endpoints": [
            "/tools/list",
            "/tools/call",
            "/resources/list",
            "/resources/read"
        ]
    }


@app.post("/tools/list")
def list_tools(request: Optional[MCPRequest] = None):
    """List all available tools."""
    return {"tools": TOOLS}


@app.post("/tools/call")
def call_tool(request: MCPRequest):
    """Call a specific tool."""
    tool_name = request.params.get("name")
    arguments = request.params.get("arguments", {})
    
    if tool_name == "calculator":
        return handle_calculator(arguments)
    elif tool_name == "weather":
        return handle_weather(arguments)
    elif tool_name == "time":
        return handle_time(arguments)
    elif tool_name == "uuid":
        return handle_uuid(arguments)
    else:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")


def handle_calculator(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle calculator tool."""
    operation = args.get("operation")
    a = args.get("a")
    b = args.get("b")
    
    if not all([operation, a is not None, b is not None]):
        return {"error": "Missing required parameters: operation, a, b"}
    
    try:
        a = float(a)
        b = float(b)
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {"error": "Division by zero"}
            result = a / b
        else:
            return {"error": f"Unknown operation: {operation}"}
        
        return {
            "result": f"{a} {operation} {b} = {result}",
            "value": result
        }
    except Exception as e:
        return {"error": str(e)}


def handle_weather(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle weather tool (simulated data)."""
    city = args.get("city", "Unknown")
    
    # Simulated weather data
    weather_data = {
        "Tokyo": {"temp": 18, "condition": "Sunny", "humidity": 65},
        "London": {"temp": 12, "condition": "Cloudy", "humidity": 80},
        "New York": {"temp": 15, "condition": "Rainy", "humidity": 75},
        "Paris": {"temp": 14, "condition": "Partly Cloudy", "humidity": 70},
        "Sydney": {"temp": 22, "condition": "Clear", "humidity": 60},
    }
    
    data = weather_data.get(city, {"temp": 20, "condition": "Clear", "humidity": 50})
    
    return {
        "result": f"Weather in {city}: {data['condition']}, {data['temp']}°C, Humidity: {data['humidity']}%",
        "city": city,
        "temperature": data['temp'],
        "condition": data['condition'],
        "humidity": data['humidity']
    }


def handle_time(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle time tool."""
    from datetime import datetime
    import pytz
    
    timezone = args.get("timezone", "UTC")
    
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return {
            "result": f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
            "timezone": timezone,
            "timestamp": current_time.isoformat()
        }
    except Exception as e:
        return {"error": f"Invalid timezone: {timezone}"}


def handle_uuid(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle UUID generation."""
    import uuid
    generated_uuid = str(uuid.uuid4())
    return {
        "result": f"Generated UUID: {generated_uuid}",
        "uuid": generated_uuid
    }


@app.post("/resources/list")
def list_resources(request: Optional[MCPRequest] = None):
    """List available resources."""
    return {
        "resources": [
            {
                "uri": "docs://readme",
                "name": "README",
                "description": "MCP Test Server documentation",
                "mimeType": "text/markdown"
            }
        ]
    }


@app.post("/resources/read")
def read_resource(request: MCPRequest):
    """Read a specific resource."""
    uri = request.params.get("uri")
    
    if uri == "docs://readme":
        content = """# MCP Test Server

This is a simple MCP server for testing MooAgent.

## Available Tools

1. **calculator** - Perform basic math operations
2. **weather** - Get weather information (simulated)
3. **time** - Get current time in any timezone
4. **uuid** - Generate random UUIDs

## Usage

Ask MooAgent to use these tools:
- "What's 15 plus 27?"
- "What's the weather in Tokyo?"
- "What time is it in New York?"
- "Generate a UUID for me"
"""
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/markdown",
                    "text": content
                }
            ]
        }
    
    raise HTTPException(status_code=404, detail=f"Resource '{uri}' not found")


if __name__ == "__main__":
    print("🚀 Starting MCP Test Server...")
    print("📍 Server will be available at: http://localhost:3001")
    print("🛠️  Available tools: calculator, weather, time, uuid")
    print("\n💡 Add this to your backend/.env file:")
    print("   MCP_SERVER_URL=http://localhost:3001")
    print("\n⏹️  Press Ctrl+C to stop\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3001,
        log_level="info"
    )
