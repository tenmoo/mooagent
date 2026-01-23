from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    groq_api_key: str
    
    # JWT Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application Configuration
    app_name: str = "MooAgent"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000"
    
    # MCP Configuration (optional)
    mcp_server_url: str = ""
    
    # Default Model
    default_model: str = "openai/gpt-oss-120b"  # Groq-hosted OpenAI model
    
    @property
    def available_models(self) -> List[dict]:
        """List of available models from Groq (including OpenAI GPT-OSS models).
        
        Source: https://console.groq.com/docs/models
        All models run on Groq's ultra-fast infrastructure.
        """
        return [
            # OpenAI GPT-OSS Models (Groq-hosted, open-weight)
            {
                "id": "openai/gpt-oss-120b",
                "name": "GPT-OSS 120B ⭐",
                "description": "OpenAI's flagship open model, 500 t/s, browser search & code execution",
                "context_window": 131072,
                "provider": "groq"
            },
            {
                "id": "openai/gpt-oss-20b",
                "name": "GPT-OSS 20B ⚡",
                "description": "Fast OpenAI model, 1000 t/s, highly efficient",
                "context_window": 131072,
                "provider": "groq"
            },
            # Meta LLaMA Models (Groq-hosted)
            {
                "id": "llama-3.3-70b-versatile",
                "name": "LLaMA 3.3 70B",
                "description": "Latest Meta model, 280 t/s",
                "context_window": 131072,
                "provider": "groq"
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "LLaMA 3.1 8B Instant",
                "description": "Fastest model, 560 t/s",
                "context_window": 131072,
                "provider": "groq"
            }
        ]
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
