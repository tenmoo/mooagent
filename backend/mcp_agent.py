"""
MCP Sub-Agent for connecting to remote Model Context Protocol servers.
Supports both simple REST-style MCP servers and FastMCP (JSON-RPC over HTTP).
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
        # Configure client to follow redirects and accept SSE
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "Accept": "application/json, text/event-stream"
            }
        )
        self._tools_cache = None
        self._server_type = None  # 'rest' or 'jsonrpc'
    
    async def _parse_sse_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        Parse Server-Sent Events (SSE) response from FastMCP.
        
        Args:
            response: HTTP response object
            
        Returns:
            Parsed JSON data from the SSE message
        """
        text = response.text
        lines = text.strip().split('\n')
        
        # Look for data: line in SSE format
        for line in lines:
            if line.startswith('data: '):
                data_str = line[6:]  # Remove 'data: ' prefix
                return json.loads(data_str)
        
        # If no SSE format, try parsing as regular JSON
        return response.json()
    
    def _format_helpx_results(self, data: Dict[str, Any]) -> str:
        """
        Format Adobe HelpX search results in a human-readable way.
        
        Args:
            data: Parsed helpx response with query, total_results, and results
            
        Returns:
            Formatted string for the agent to use
        """
        query = data.get("query", "your query")
        total = data.get("total_results", 0)
        results = data.get("results", [])
        
        if total == 0:
            return f"No Adobe HelpX documentation found for '{query}'. Try rephrasing your question."
        
        output = [f"Found {total} Adobe HelpX articles about '{query}':\n"]
        
        for i, result in enumerate(results[:5], 1):  # Show top 5
            title = result.get("title", "No title")
            url = result.get("url", "")
            score = result.get("score", 0.0)
            snippet = result.get("snippet", "")
            
            output.append(f"\n{i}. **{title}**")
            if url:
                output.append(f"   🔗 {url}")
            output.append(f"   📊 Relevance: {score:.2f}")
            if snippet:
                # Truncate snippet if too long
                clean_snippet = snippet.strip()
                if len(clean_snippet) > 200:
                    clean_snippet = clean_snippet[:200] + "..."
                output.append(f"   📝 {clean_snippet}")
        
        return "\n".join(output)
    
    async def _detect_server_type(self) -> str:
        """
        Detect if the server is REST-style or JSON-RPC style.
        
        Returns:
            'rest' or 'jsonrpc'
        """
        if self._server_type:
            return self._server_type
        
        print(f"🔍 Detecting MCP server type at {self.mcp_url}...")
        
        # Try JSON-RPC style first (FastMCP)
        try:
            print(f"   Trying JSON-RPC format...")
            response = await self.client.post(
                self.mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {},
                    "id": 1
                },
                headers={"Content-Type": "application/json"}
            )
            print(f"   JSON-RPC response status: {response.status_code}")
            
            if response.status_code == 200:
                # Try parsing as SSE first
                data = await self._parse_sse_response(response)
                print(f"   JSON-RPC response keys: {list(data.keys())}")
                if "result" in data or "error" in data or "jsonrpc" in data:
                    self._server_type = 'jsonrpc'
                    print(f"✅ Detected JSON-RPC MCP server at {self.mcp_url}")
                    return 'jsonrpc'
        except Exception as e:
            print(f"   JSON-RPC detection failed: {e}")
        
        # Try REST style
        try:
            print(f"   Trying REST format...")
            response = await self.client.post(
                f"{self.mcp_url}/tools/list",
                json={"method": "tools/list"},
                headers={"Content-Type": "application/json"}
            )
            print(f"   REST response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   REST response keys: {list(data.keys())}")
                if "tools" in data or "result" in data:
                    self._server_type = 'rest'
                    print(f"✅ Detected REST-style MCP server at {self.mcp_url}")
                    return 'rest'
        except Exception as e:
            print(f"   REST detection failed: {e}")
        
        # Default to JSON-RPC if URL ends with /mcp
        if self.mcp_url.endswith('/mcp'):
            print(f"⚠️  Auto-detection inconclusive, defaulting to JSON-RPC (URL ends with /mcp)")
            self._server_type = 'jsonrpc'
            return 'jsonrpc'
        
        # Otherwise default to REST
        print(f"⚠️  Auto-detection inconclusive, defaulting to REST")
        self._server_type = 'rest'
        return 'rest'
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools from the MCP server.
        
        Returns:
            List of tool definitions
        """
        if not self.mcp_url:
            return []
        
        try:
            server_type = await self._detect_server_type()
            print(f"🔍 Listing tools from MCP server ({server_type}): {self.mcp_url}")
            
            if server_type == 'jsonrpc':
                # JSON-RPC style (FastMCP)
                response = await self.client.post(
                    self.mcp_url,
                    json={
                        "jsonrpc": "2.0",
                        "method": "tools/list",
                        "params": {},
                        "id": 1
                    },
                    headers={"Content-Type": "application/json"}
                )
            else:
                # REST style
                response = await self.client.post(
                    f"{self.mcp_url}/tools/list",
                    json={"method": "tools/list"},
                    headers={"Content-Type": "application/json"}
                )
            
            response.raise_for_status()
            
            # Parse response (SSE or JSON)
            if server_type == 'jsonrpc':
                data = await self._parse_sse_response(response)
            else:
                data = response.json()
            
            # Debug logging
            print(f"📦 MCP Response keys: {list(data.keys())}")
            
            # Handle different response formats
            if server_type == 'jsonrpc':
                # JSON-RPC format: {"jsonrpc": "2.0", "result": {"tools": [...]}, "id": 1}
                if "result" in data:
                    result = data["result"]
                    if isinstance(result, dict) and "tools" in result:
                        tools = result["tools"]
                    elif isinstance(result, list):
                        tools = result
                    else:
                        print(f"⚠️  Unexpected JSON-RPC result format: {result}")
                        tools = []
                elif "error" in data:
                    print(f"❌ JSON-RPC error: {data['error']}")
                    tools = []
                else:
                    print(f"⚠️  Unexpected JSON-RPC response: {data}")
                    tools = []
            else:
                # REST format
                if "tools" in data:
                    tools = data["tools"]
                elif "result" in data and isinstance(data["result"], dict) and "tools" in data["result"]:
                    tools = data["result"]["tools"]
                elif "result" in data and isinstance(data["result"], list):
                    tools = data["result"]
                else:
                    print(f"⚠️  Unexpected REST response format. Keys: {list(data.keys())}")
                    tools = []
            
            self._tools_cache = tools
            print(f"✅ Found {len(tools)} tools from MCP server:")
            for tool in tools:
                print(f"   - {tool.get('name', 'unnamed')}: {tool.get('description', 'no description')[:100]}")
            return self._tools_cache
        except Exception as e:
            print(f"❌ Error listing MCP tools: {e}")
            import traceback
            traceback.print_exc()
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
            server_type = await self._detect_server_type()
            
            print(f"🔧 Calling MCP tool: {tool_name}")
            print(f"📦 Arguments: {arguments}")
            print(f"🌐 MCP URL: {self.mcp_url} ({server_type})")
            
            if server_type == 'jsonrpc':
                # JSON-RPC style (FastMCP)
                payload = {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    },
                    "id": 2
                }
                response = await self.client.post(
                    self.mcp_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
            else:
                # REST style
                payload = {
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                }
                response = await self.client.post(
                    f"{self.mcp_url}/tools/call",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
            
            response.raise_for_status()
            
            # Parse response (SSE or JSON)
            if server_type == 'jsonrpc':
                data = await self._parse_sse_response(response)
            else:
                data = response.json()
            
            print(f"✅ MCP Response: {data}")
            
            # Extract result based on server type
            if server_type == 'jsonrpc':
                # JSON-RPC format: {"jsonrpc": "2.0", "result": {...}, "id": 2}
                if "result" in data:
                    result = data["result"]
                    if isinstance(result, dict):
                        # Check for nested 'content' field (FastMCP tool response format)
                        if "content" in result:
                            content = result["content"]
                            if isinstance(content, list) and len(content) > 0:
                                # Extract text from content array
                                text = content[0].get("text", json.dumps(content, indent=2))
                                
                                # Try to parse as JSON for better formatting
                                try:
                                    parsed = json.loads(text)
                                    # Format helpx results nicely
                                    if isinstance(parsed, dict) and "results" in parsed:
                                        return self._format_helpx_results(parsed)
                                    return text
                                except (json.JSONDecodeError, TypeError):
                                    return text
                            return str(content)
                        # Check for nested 'result' field
                        if "result" in result:
                            return str(result["result"])
                        # Return formatted dict
                        return json.dumps(result, indent=2)
                    return str(result)
                elif "error" in data:
                    error = data["error"]
                    return f"MCP Error: {error.get('message', error)}"
            else:
                # REST format
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
            
            # Adobe HelpX detection (check this first as it's most specific)
            adobe_products = [
                'photoshop', 'illustrator', 'indesign', 'acrobat', 'premiere', 
                'after effects', 'aftereffects', 'lightroom', 'xd', 'substance',
                'animate', 'audition', 'bridge', 'camera raw', 'experience manager',
                'aem', 'target', 'analytics', 'marketo', 'sign', 'dimension',
                'fresco', 'express', 'creative cloud', 'adobe'
            ]
            
            helpx_keywords = [
                'how to', 'how do i', 'crop', 'edit', 'create', 'export', 'import',
                'save', 'open', 'layer', 'mask', 'brush', 'tool', 'effect',
                'filter', 'adjustment', 'color', 'transform', 'resize', 'rotate'
            ]
            
            is_adobe_query = any(product in query_lower for product in adobe_products)
            is_helpx_query = any(keyword in query_lower for keyword in helpx_keywords)
            
            if is_adobe_query or is_helpx_query:
                tool_name = "helpx"
                # Pass the full query to helpx
                arguments = {"query": tool_query, "top_k": 5}
                print(f"🎯 Detected Adobe HelpX query: '{tool_query}'")
            
            # Calculator detection
            elif any(word in query_lower for word in ['calculate', 'calculator', 'add', 'subtract', 'multiply', 'divide', '+', '-', '*', '/', 'plus', 'minus', 'times']):
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
            
            # Adobe region detection
            elif 'adobe region' in query_lower or ('region' in query_lower and any(r in query_lower for r in ['us-east', 'us-west', 'eastus', 'westus'])):
                tool_name = "get_adobe_region"
                # Extract region from query
                import re
                region_match = re.search(r'(us-east-\d|us-west-\d|eastus\d?|westus\d?)', query_lower)
                if region_match:
                    arguments = {"cloud_region": region_match.group(1)}
                else:
                    arguments = {"query": tool_query}
            
            if not tool_name:
                return f"Could not determine which tool to use from query: {tool_query}. Available tools: helpx (Adobe product help), calculator, weather, time, uuid, get_adobe_region"
            
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
            
            print(f"📤 MCP Result: {result[:500]}..." if len(result) > 500 else f"📤 MCP Result: {result}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error calling MCP tool: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg
