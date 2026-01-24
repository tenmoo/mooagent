from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Dict, Any

from config import settings
from models import (
    UserCreate, UserLogin, User, Token,
    ChatRequest, ChatResponse
)
from auth import (
    create_access_token, authenticate_user, create_user,
    get_current_user
)
from agent import moo_agent

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered personal assistant API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/auth/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate) -> User:
    """Register a new user."""
    try:
        user = create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        return user
    except HTTPException:
        # Re-raise HTTP exceptions (like "email already registered")
        raise
    except Exception as e:
        # Log and return other errors
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )


@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin) -> Token:
    """Login and get access token."""
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token)


@app.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    """Get current user information."""
    return current_user


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Chat with the AI agent.
    
    This endpoint processes user messages and returns AI-generated responses.
    Optionally accepts a model parameter to use a specific LLM model.
    """
    try:
        # Log the incoming request
        print(f"📨 Chat request from user: {current_user.email}")
        print(f"📝 Message: {request.message[:50]}..." if len(request.message) > 50 else f"📝 Message: {request.message}")
        print(f"🤖 Current model: {moo_agent.current_model}")
        
        # If a model is specified and different from current, switch models
        if request.model:
            print(f"🔍 Requested model: {request.model}")
            if request.model != moo_agent.current_model:
                print(f"🔄 Model switch needed: {moo_agent.current_model} → {request.model}")
                moo_agent.set_model(request.model)
            else:
                print(f"✅ Already using requested model: {request.model}")
        
        response = moo_agent.chat(
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        print(f"✅ Response generated successfully")
        
        return ChatResponse(
            response=response,
            conversation_id=None  # Could generate/track conversation IDs in production
        )
    except Exception as e:
        error_msg = str(e)
        
        # Check if it's a model decommissioned error
        if "model_decommissioned" in error_msg or "has been decommissioned" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The selected model is no longer available. Please choose a different model from the model selector. Error: {error_msg}"
            )
        
        # Log the full error for debugging
        print(f"❌ Chat error: {error_msg}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {error_msg}"
        )


@app.get("/agent/info")
async def get_agent_info(
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """Get information about the AI agent."""
    return {
        "name": "MooAgent",
        "description": "AI-powered personal assistant",
        "system_prompt": moo_agent.get_system_prompt(),
        "model": moo_agent.current_model
    }


@app.get("/agent/models")
async def get_available_models(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get list of available LLM models."""
    return {
        "models": settings.available_models,
        "current_model": moo_agent.current_model,
        "default_model": settings.default_model
    }


@app.get("/agent/tools")
async def get_agent_tools(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get information about available agent tools including MCP tools."""
    from typing import Any
    
    tools_info = {
        "built_in_tools": [
            {
                "name": "AssistantHelper",
                "description": "A helpful assistant that can help with various daily work tasks, answer questions, and provide information."
            }
        ],
        "mcp_tools": [],
        "mcp_server_url": settings.mcp_server_url or None
    }
    
    # Get MCP tools if available
    if settings.mcp_server_url:
        try:
            from mcp_agent import MCPSubAgent
            mcp_agent_instance = MCPSubAgent(settings.mcp_server_url)
            mcp_tools = await mcp_agent_instance.list_tools()
            tools_info["mcp_tools"] = mcp_tools
            await mcp_agent_instance.close()
        except Exception as e:
            print(f"Error fetching MCP tools: {e}")
            tools_info["mcp_error"] = str(e)
    
    return tools_info


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
