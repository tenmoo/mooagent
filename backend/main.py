from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Dict

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
    """
    try:
        response = moo_agent.chat(
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            response=response,
            conversation_id=None  # Could generate/track conversation IDs in production
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
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
        "model": "Groq LLaMA 3 70B"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
