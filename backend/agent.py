from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from typing import List, Dict
from config import settings
from models import ChatMessage


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
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=settings.debug,
            max_iterations=3,
            early_stopping_method="generate",
        )
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent."""
        return [
            Tool(
                name="AssistantHelper",
                func=self._assistant_helper,
                description="A helpful assistant that can help with various daily work tasks, answer questions, and provide information."
            )
        ]
    
    def _assistant_helper(self, query: str) -> str:
        """Assistant helper function."""
        return f"I'm here to help you with: {query}. This is a demo response. In production, this would connect to real tools and APIs."
    
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
            
            # Get response from agent
            if conversation_history:
                # Use agent with memory for conversation
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
                
                # Add history to memory
                for msg in conversation_history:
                    if msg.role == "user":
                        memory.chat_memory.add_user_message(msg.content)
                    elif msg.role == "assistant":
                        memory.chat_memory.add_ai_message(msg.content)
                
                # Use invoke instead of deprecated run
                response = self.agent.invoke({
                    "input": message,
                    "chat_history": memory.chat_memory.messages
                })
                # Extract the output from the response
                if isinstance(response, dict):
                    response = response.get("output", str(response))
                else:
                    response = str(response)
            else:
                # Direct LLM call for simple queries
                response = self.llm.invoke(messages)
                response = response.content
            
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
