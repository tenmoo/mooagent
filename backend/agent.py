from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain import hub
from typing import List, Dict
from config import settings
from models import ChatMessage
from mcp_agent import MCPToolWrapper


class MooAgent:
    """AI Agent powered by Groq and LangChain."""
    
    def __init__(self):
        """Initialize the MooAgent."""
        # Try to use the latest available model
        # Check https://console.groq.com/docs/models for current models
        try:
            self.llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                groq_api_key=settings.groq_api_key
            )
        except Exception as e:
            print(f"Warning: Could not initialize llama-3.3-70b-versatile, trying fallback model: {e}")
            # Fallback to a commonly available model
            self.llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.7,
                groq_api_key=settings.groq_api_key
            )
        
        # Define tools for the agent
        self.tools = self._create_tools()
        
        # Get the react prompt template
        # This is the standard ReAct prompt from LangChain hub
        try:
            prompt = hub.pull("hwchase17/react-chat")
        except:
            # Fallback to a custom prompt if hub is not accessible
            from langchain.prompts import PromptTemplate
            template = """Assistant is a large language model trained by Groq.

Assistant is designed to be helpful, harmless, and honest. Assistant should always be polite and respectful.

TOOLS:
------

Assistant has access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}"""
            
            prompt = PromptTemplate(
                template=template,
                input_variables=["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]
            )
        
        # Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the agent executor
        self.agent = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=settings.debug,
            max_iterations=10,  # Increased from 3 to 10
            max_execution_time=30,  # 30 second timeout
            handle_parsing_errors=True,
            return_intermediate_steps=True  # Return tool usage details
        )
    
    def _create_tools(self) -> List:
        """Create tools for the agent."""
        from langchain.tools import Tool
        
        tools = [
            Tool(
                name="AssistantHelper",
                func=self._assistant_helper,
                description="A helpful assistant that can help with various daily work tasks, answer questions, and provide information."
            )
        ]
        
        # Add MCP tool if configured
        if settings.mcp_server_url:
            try:
                mcp_wrapper = MCPToolWrapper(settings.mcp_server_url)
                tools.append(
                    Tool(
                        name="MCPRemoteTool",
                        func=mcp_wrapper.call_mcp_tool,
                        description=f"Call remote MCP server tools at {settings.mcp_server_url}. Use this to access external tools and resources. Input should be a natural language description of what you want to do."
                    )
                )
                print(f"✅ MCP sub-agent initialized with server: {settings.mcp_server_url}")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize MCP sub-agent: {e}")
        
        return tools
    
    def _assistant_helper(self, query: str) -> str:
        """Assistant helper function."""
        # For simple queries that don't need external tools
        return f"I can help you with: {query}. Let me know if you need specific calculations, weather info, time, or UUID generation - I have tools for those!"
    
    def chat(self, message: str, conversation_history: List[ChatMessage] = None) -> str:
        """
        Process a chat message and return a response.
        
        Args:
            message: The user's message
            conversation_history: Optional list of previous messages
        
        Returns:
            The agent's response
        """
        try:
            # Convert conversation history to LangChain format
            messages = []
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    if msg.role == "system":
                        messages.append(SystemMessage(content=msg.content))
                    elif msg.role == "user":
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role == "assistant":
                        messages.append(AIMessage(content=msg.content))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Always use the agent (even for first message) to enable tool usage
            # Build chat history string
            chat_history = ""
            if conversation_history:
                for msg in conversation_history:
                    if msg.role == "user":
                        chat_history += f"Human: {msg.content}\n"
                    elif msg.role == "assistant":
                        chat_history += f"Assistant: {msg.content}\n"
            
            print(f"\n{'='*60}")
            print(f"🤖 Agent Processing Query: {message}")
            print(f"📚 Conversation History Length: {len(conversation_history) if conversation_history else 0}")
            print(f"{'='*60}\n")
            
            # Use invoke with the new agent executor
            response = self.agent.invoke({
                "input": message,
                "chat_history": chat_history
            })
            
            print(f"\n{'='*60}")
            print(f"📊 Agent Response Object Type: {type(response)}")
            print(f"📊 Agent Response Keys: {response.keys() if isinstance(response, dict) else 'N/A'}")
            
            if isinstance(response, dict) and 'intermediate_steps' in response:
                print(f"🔧 Tool Usage Steps: {len(response['intermediate_steps'])}")
                for i, (action, observation) in enumerate(response['intermediate_steps'], 1):
                    print(f"\n  Step {i}:")
                    print(f"    Tool: {action.tool}")
                    print(f"    Input: {action.tool_input[:100]}...")
                    print(f"    Output: {str(observation)[:200]}...")
            
            print(f"{'='*60}\n")
            
            # Extract the output from the response
            if isinstance(response, dict):
                response = response.get("output", str(response))
            else:
                response = str(response)
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            print(f"AGENT ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            if settings.debug:
                raise
            return f"I apologize, but I encountered an error: {str(e)}. Please check your API configuration."
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """You are MooAgent, an AI-powered personal assistant designed to help with daily work tasks.
        
Your capabilities include:
- Answering questions and providing information
- Helping with task planning and organization
- Providing guidance and advice
- Assisting with various work-related queries

You are friendly, helpful, and professional. Always aim to provide clear, concise, and actionable responses.
If you're unsure about something, be honest and suggest alternatives."""


# Global agent instance
moo_agent = MooAgent()
