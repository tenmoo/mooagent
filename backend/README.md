# MooAgent Backend

AI-powered personal assistant backend built with FastAPI, Groq, and LangChain.

## Features

- 🤖 AI agent powered by OpenAI GPT-OSS & Meta LLaMA via Groq
- 🔄 Multiple model selection (GPT-OSS 120B/20B, LLaMA 3.3 70B/3.1 8B)
- 🔐 JWT-based authentication
- 💬 Conversational AI with context memory
- 🔌 Model Context Protocol (MCP) integration
- 🚀 FastAPI for high performance
- 📝 Full OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI
- **AI/LLM**: Groq (OpenAI GPT-OSS & Meta LLaMA models)
- **AI Framework**: LangChain
- **Authentication**: JWT with OAuth 2.0 pattern
- **Deployment**: Fly.io

## Setup

### Prerequisites

- Python 3.9+
- Groq API key (get from https://console.groq.com)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Edit `.env` and add your configuration:
```env
GROQ_API_KEY=your_actual_groq_api_key
SECRET_KEY=your_generated_secret_key
```

Generate a secret key with:
```bash
openssl rand -hex 32
```

### Running Locally

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info

### Chat

- `POST /chat` - Chat with the AI agent (supports model parameter)
- `GET /agent/info` - Get agent information and current model
- `GET /agent/tools` - List all available tools (including MCP)
- `GET /agent/models` - List all available LLM models

### Health

- `GET /` - Root endpoint
- `GET /health` - Health check

## Deployment to Fly.io

### Prerequisites

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to Fly:
```bash
fly auth login
```

### Deploy

1. Launch the app (first time):
```bash
fly launch
```

2. Set environment secrets:
```bash
fly secrets set GROQ_API_KEY=your_groq_api_key
fly secrets set SECRET_KEY=your_secret_key
fly secrets set ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

3. Deploy:
```bash
fly deploy
```

4. Check status:
```bash
fly status
fly logs
```

### Scale (Optional)

```bash
fly scale vm shared-cpu-1x --memory 512
fly scale count 1
```

## Development

### Project Structure

```
backend/
├── main.py           # FastAPI application and routes
├── config.py         # Configuration and settings
├── models.py         # Pydantic models
├── auth.py           # Authentication logic
├── agent.py          # AI agent implementation
├── mcp_agent.py      # MCP sub-agent for remote tools
├── requirements.txt  # Python dependencies
├── fly.toml          # Fly.io configuration
└── .env.example      # Environment variables template
```

### Adding New Features

1. Define models in `models.py`
2. Add business logic in appropriate modules
3. Create endpoints in `main.py`
4. Update documentation

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS configured for allowed origins
- Environment variables for sensitive data
- HTTPS enforced in production

## License

MIT
