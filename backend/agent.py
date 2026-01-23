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
    
    def __init__(self, model: str = None):
        """Initialize the MooAgent with optional model selection.
        
        Args:
            model: Model ID to use. If None, uses default from settings.
        """
        self.current_model = model or settings.default_model
        self.llm = self._initialize_llm(self.current_model)
        
        # Define tools for the agent
        self.tools = self._create_tools()
        
        # Get the react prompt template
        # This is the standard ReAct prompt from LangChain hub
        try:
            prompt = hub.pull("hwchase17/react-chat")
        except:
            # Fallback to a custom prompt if hub is not accessible
            from langchain.prompts import PromptTemplate
            template = """You are a helpful AI assistant with access to tools.

TOOLS:
------
You have access to the following tools:

{tools}

RESPONSE FORMAT:
----------------
To use a tool, you MUST use this exact format:

Thought: [your reasoning about what to do]
Action: [tool name - must be one of: {tool_names}]
Action Input: [the input to the tool]

After you see the Observation, you can continue thinking and acting, or provide a final answer.

To respond without using a tool, you MUST use this exact format:

Thought: [your reasoning]
Final Answer: [your response to the user]

IMPORTANT RULES:
- ALWAYS include "Thought:" before your reasoning
- ALWAYS include "Action:" when using a tool
- ALWAYS include "Final Answer:" when responding directly
- Do NOT skip any of these labels
- Do NOT add extra text outside the format

Previous conversation:
{chat_history}

User: {input}

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
        
        # Create the agent executor with better error handling
        self.agent = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=settings.debug,
            max_iterations=10,
            max_execution_time=30,
            handle_parsing_errors="Check your output and make sure it conforms to the format instructions. If you want to respond directly, use 'Final Answer: your response'",
            return_intermediate_steps=True
        )
    
    def _initialize_llm(self, model: str):
        """Initialize the LLM with the specified model through Groq.
        
        All models (including OpenAI GPT-OSS) run on Groq's infrastructure.
        
        Args:
            model: Model ID to use (e.g., "openai/gpt-oss-120b", "llama-3.3-70b-versatile")
            
        Returns:
            Initialized ChatGroq instance
        """
        try:
            llm = ChatGroq(
                model=model,
                temperature=0.7,
                groq_api_key=settings.groq_api_key
            )
            print(f"✅ Initialized Groq LLM with model: {model}")
            return llm
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize {model}, trying fallback: {e}")
            # Fallback to the fastest model
            fallback_model = "llama-3.1-8b-instant"
            llm = ChatGroq(
                model=fallback_model,
                temperature=0.7,
                groq_api_key=settings.groq_api_key
            )
            print(f"✅ Using fallback model: {fallback_model}")
            return llm
    
    def set_model(self, model: str):
        """Change the LLM model dynamically.
        
        Args:
            model: Model ID to switch to
        """
        self.current_model = model
        self.llm = self._initialize_llm(model)
        # Reinitialize the agent with the new LLM
        self.__init__(model=model)
    
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
                
                # Build dynamic description based on available tools
                tool_description = """Access remote MCP server tools for:
- Adobe HelpX: Search Adobe product documentation (Photoshop, Illustrator, Acrobat, etc.). Use for questions like "how to crop in Photoshop" or "create PDF in Acrobat"
- Calculator: Perform mathematical calculations
- Weather: Get weather information for cities
- Time: Get current time information
- UUID: Generate unique identifiers
- Adobe Regions: Get Adobe region names for cloud regions

Input should be a natural language description of what you want to do."""
                
                tools.append(
                    Tool(
                        name="MCPRemoteTool",
                        func=mcp_wrapper.call_mcp_tool,
                        description=tool_description
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
