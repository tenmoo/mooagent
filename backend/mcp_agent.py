"""
MCP Sub-Agent for connecting to remote Model Context Protocol servers.
"""
from typing import Dict, Any, Optional, List
import httpx
import json
from config import settings


class MCPSubAgent:
    """Sub-agent for interacting with remote MCP servers."""
    
    def __init__(self, mcp_url: Optional[str] = None):
        """
        Initialize MCP sub-agent.
        
        Args:
            mcp_url: URL of the remote MCP server
        """
        self.mcp_url = mcp_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self._tools_cache = None
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools from the MCP server.
        
        Returns:
            List of tool definitions
        """
        if not self.mcp_url:
            return []
        
        try:
            response = await self.client.post(
                f"{self.mcp_url}/tools/list",
                json={"method": "tools/list"},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            self._tools_cache = data.get("tools", [])
            return self._tools_cache
        except Exception as e:
            print(f"Error listing MCP tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Call a specific tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
        
        Returns:
            Tool execution result as string
        """
        if not self.mcp_url:
            return "Error: No MCP server URL configured"
        
        try:
            payload = {
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            print(f"🔧 Calling MCP tool: {tool_name}")
            print(f"📦 Arguments: {arguments}")
            print(f"🌐 MCP URL: {self.mcp_url}")
            
            response = await self.client.post(
                f"{self.mcp_url}/tools/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ MCP Response: {data}")
            
            # Extract result from MCP response
            if "result" in data:
                result = data["result"]
                if isinstance(result, dict):
                    # If result is a dict, check for nested 'result' field first
                    if "result" in result:
                        return str(result["result"])
                    # Otherwise return a formatted version
                    return json.dumps(result, indent=2)
                return str(result)
            
            # If no 'result' field, return the whole response
            return json.dumps(data, indent=2)
            
        except httpx.HTTPError as e:
            error_msg = f"HTTP Error calling MCP tool '{tool_name}': {str(e)}"
            print(f"❌ {error_msg}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return error_msg
        except Exception as e:
            error_msg = f"Error calling MCP tool '{tool_name}': {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg
    
    async def get_resources(self) -> List[Dict[str, Any]]:
        """
        Get available resources from the MCP server.
        
        Returns:
            List of resource definitions
        """
        if not self.mcp_url:
            return []
        
        try:
            response = await self.client.post(
                f"{self.mcp_url}/resources/list",
                json={"method": "resources/list"},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("resources", [])
        except Exception as e:
            print(f"Error listing MCP resources: {e}")
            return []
    
    async def read_resource(self, resource_uri: str) -> str:
        """
        Read a specific resource from the MCP server.
        
        Args:
            resource_uri: URI of the resource to read
        
        Returns:
            Resource content as string
        """
        if not self.mcp_url:
            return "Error: No MCP server URL configured"
        
        try:
            payload = {
                "method": "resources/read",
                "params": {
                    "uri": resource_uri
                }
            }
            
            response = await self.client.post(
                f"{self.mcp_url}/resources/read",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            if "contents" in data:
                contents = data["contents"]
                if isinstance(contents, list) and len(contents) > 0:
                    return contents[0].get("text", str(contents))
                return str(contents)
            
            return json.dumps(data, indent=2)
            
        except Exception as e:
            return f"Error reading MCP resource '{resource_uri}': {str(e)}"
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
            else:
                loop.run_until_complete(self.close())
        except:
            pass


# Synchronous wrapper for LangChain tool compatibility
class MCPToolWrapper:
    """Synchronous wrapper for MCP sub-agent for use with LangChain."""
    
    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url
    
    def _call_async(self, coro):
        """Helper to run async code in sync context using a thread."""
        import asyncio
        import threading
        from concurrent.futures import Future
        
        # Create a future to get the result
        future = Future()
        
        def run_in_thread():
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(coro)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                loop.close()
        
        # Run in a separate thread
        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join(timeout=30)  # 30 second timeout
        
        if thread.is_alive():
            raise TimeoutError("MCP tool call timed out after 30 seconds")
        
        return future.result()
    
    def call_mcp_tool(self, tool_query: str) -> str:
        """
        Call an MCP tool with a natural language query.
        
        Args:
            tool_query: Natural language description of what to do
        
        Returns:
            Result from the MCP tool
        """
        try:
            # Extract tool name and arguments from the query
            query_lower = tool_query.lower()
            
            # Simple keyword-based tool detection
            tool_name = None
            arguments = {}
            
            # Calculator detection
            if any(word in query_lower for word in ['calculate', 'calculator', 'add', 'subtract', 'multiply', 'divide', '+', '-', '*', '/', 'plus', 'minus', 'times']):
                tool_name = "calculator"
                # Try to extract numbers and operation
                if 'add' in query_lower or '+' in query_lower or 'plus' in query_lower:
                    arguments = {"operation": "add", "query": tool_query}
                elif 'subtract' in query_lower or '-' in query_lower or 'minus' in query_lower:
                    arguments = {"operation": "subtract", "query": tool_query}
                elif 'multiply' in query_lower or '*' in query_lower or 'times' in query_lower:
                    arguments = {"operation": "multiply", "query": tool_query}
                elif 'divide' in query_lower or '/' in query_lower:
                    arguments = {"operation": "divide", "query": tool_query}
                else:
                    arguments = {"query": tool_query}
            
            # Weather detection
            elif 'weather' in query_lower:
                tool_name = "weather"
                # Try to extract city name
                for city in ['tokyo', 'london', 'new york', 'paris', 'sydney']:
                    if city in query_lower:
                        arguments = {"city": city.title()}
                        break
                if not arguments:
                    arguments = {"query": tool_query}
            
            # Time detection
            elif 'time' in query_lower or 'clock' in query_lower:
                tool_name = "time"
                arguments = {"query": tool_query}
            
            # UUID detection
            elif 'uuid' in query_lower or 'unique id' in query_lower or 'identifier' in query_lower:
                tool_name = "uuid"
                arguments = {}
            
            if not tool_name:
                return f"Could not determine which tool to use from query: {tool_query}. Please try: 'calculate X + Y', 'weather in [city]', 'what time is it', or 'generate uuid'"
            
            print(f"🎯 Detected tool: {tool_name} with arguments: {arguments}")
            
            # Create a new MCP agent for each call to avoid connection issues
            async def make_call():
                agent = MCPSubAgent(self.mcp_url)
                try:
                    result = await agent.call_tool(tool_name, arguments)
                    return result
                finally:
                    await agent.close()
            
            # Call the async method in a separate thread
            result = self._call_async(make_call())
            
            print(f"📤 MCP Result: {result}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error calling MCP tool: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg
