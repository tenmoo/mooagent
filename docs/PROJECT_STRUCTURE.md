# MooAgent - Project Structure

Complete overview of the MooAgent project structure and files.

## Directory Tree

```
mooagent/
├── backend/                     # FastAPI backend application
│   ├── main.py                  # Main application and API routes
│   ├── agent.py                 # AI agent implementation with Groq/LangChain
│   ├── mcp_agent.py            # MCP sub-agent for remote tool integration
│   ├── auth.py                  # Authentication logic and JWT handling
│   ├── models.py                # Pydantic data models
│   ├── config.py                # Configuration and settings
│   ├── requirements.txt         # Python dependencies
│   ├── env.example             # Environment variables template
│   ├── .gitignore              # Git ignore rules for backend
│   ├── fly.toml                # Fly.io deployment configuration
│   ├── Procfile                # Process file for deployment
│   ├── start.sh                # Startup script for deployment
│   └── README.md               # Backend documentation
│
├── frontend/                    # React TypeScript frontend
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── Login.tsx       # Login page
│   │   │   ├── Register.tsx    # Registration page
│   │   │   └── Chat.tsx        # Main chat interface with tool display
│   │   ├── services/
│   │   │   └── api.ts          # API client and HTTP service
│   │   ├── store/
│   │   │   ├── authStore.ts    # Authentication state management
│   │   │   └── chatStore.ts    # Chat state management
│   │   ├── styles/
│   │   │   ├── Auth.css        # Authentication pages styling
│   │   │   └── Chat.css        # Chat interface styling (with tools panel)
│   │   ├── App.tsx             # Main app component and routing
│   │   ├── main.tsx            # Application entry point
│   │   └── index.css           # Global styles (dark theme)
│   ├── public/                 # Static assets
│   ├── index.html              # HTML template
│   ├── package.json            # Node.js dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tsconfig.node.json      # TypeScript config for Node
│   ├── vite.config.ts          # Vite build configuration
│   ├── env.example            # Environment variables template
│   ├── .gitignore             # Git ignore rules for frontend
│   ├── vercel.json            # Vercel deployment configuration
│   └── README.md              # Frontend documentation
│
├── test-mcp-server/           # Test MCP server for development
│   ├── mcp_test_server.py     # FastAPI MCP server with example tools
│   ├── requirements.txt        # Server dependencies
│   └── README.md              # Test server documentation
│
├── docs/                       # Project documentation
│   ├── prd.md                 # Product requirements document
│   ├── example.md             # Example/reference document
│   ├── GETTING_STARTED.md     # Setup and installation guide
│   ├── DEPLOYMENT.md          # Production deployment guide
│   ├── API.md                 # API documentation
│   ├── MCP_INTEGRATION.md     # MCP sub-agent integration guide
│   ├── ARCHITECTURE.md        # Architecture diagrams
│   ├── PROJECT_STRUCTURE.md   # File structure guide (this file)
│   └── QUICK_REFERENCE.md     # Quick commands reference
│
├── app.py                     # Original prototype/reference
├── README.md                  # Main project documentation
├── IMPLEMENTATION_SUMMARY.md  # Implementation summary
├── CHECKLIST.md              # Project completion checklist
├── .gitignore                # Global git ignore rules
├── start-dev.sh              # Development startup script (Unix/Mac)
└── start-dev.bat             # Development startup script (Windows)
```
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── .gitignore              # Git ignore rules for backend
│   ├── fly.toml                # Fly.io deployment configuration
│   ├── Procfile                # Process file for deployment
│   ├── start.sh                # Startup script for deployment
│   └── README.md               # Backend documentation
│
├── frontend/                    # React TypeScript frontend
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── Login.tsx       # Login page
│   │   │   ├── Register.tsx    # Registration page
│   │   │   └── Chat.tsx        # Main chat interface
│   │   ├── services/
│   │   │   └── api.ts          # API client and HTTP service
│   │   ├── store/
│   │   │   ├── authStore.ts    # Authentication state management
│   │   │   └── chatStore.ts    # Chat state management
│   │   ├── styles/
│   │   │   ├── Auth.css        # Authentication pages styling
│   │   │   └── Chat.css        # Chat interface styling
│   │   ├── App.tsx             # Main app component and routing
│   │   ├── main.tsx            # Application entry point
│   │   └── index.css           # Global styles
│   ├── public/                 # Static assets
│   ├── index.html              # HTML template
│   ├── package.json            # Node.js dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tsconfig.node.json      # TypeScript config for Node
│   ├── vite.config.ts          # Vite build configuration
│   ├── .env.example            # Environment variables template
│   ├── .gitignore             # Git ignore rules for frontend
│   ├── vercel.json            # Vercel deployment configuration
│   └── README.md              # Frontend documentation
│
├── docs/                       # Project documentation
│   ├── prd.md                 # Product requirements document
│   ├── example.md             # Example/reference document
│   ├── GETTING_STARTED.md     # Setup and installation guide
│   ├── DEPLOYMENT.md          # Production deployment guide
│   └── API.md                 # API documentation
│
├── app.py                     # Original prototype/reference
├── README.md                  # Main project documentation
├── .gitignore                # Global git ignore rules
├── start-dev.sh              # Development startup script (Unix/Mac)
└── start-dev.bat             # Development startup script (Windows)
```

## File Descriptions

### Backend Files

#### `main.py`
Main FastAPI application with all API endpoints:
- Health check and info endpoints
- Authentication endpoints (register, login, get user)
- Chat endpoint for AI interactions
- Agent info endpoint
- CORS middleware configuration

#### `agent.py`
AI agent implementation:
- MooAgent class with Groq integration (OpenAI GPT-OSS & Meta LLaMA models)
- LangChain agent setup with create_react_agent
- Tool definitions for the agent (including MCP tools)
- Dynamic model switching capability
- Conversation history management
- System prompt configuration
- Model fallback mechanism

#### `mcp_agent.py`
MCP sub-agent for remote tool integration:
- MCPSubAgent class for async MCP communication
- Tool discovery and execution
- Resource access and reading
- HTTP client with proper error handling
- Synchronous wrapper for LangChain compatibility
- Support for Model Context Protocol (MCP)

#### `auth.py`
Authentication and security:
- Password hashing with bcrypt
- JWT token creation and validation
- User authentication functions
- User creation and management
- In-memory user storage (demo)

#### `models.py`
Pydantic models for data validation:
- User models (create, login, response)
- Token models
- Chat message and request/response models
- Type-safe data structures

#### `config.py`
Application configuration:
- Environment variable loading
- Settings management with Pydantic
- CORS origins parsing
- Default values

#### `requirements.txt`
Python dependencies:
- FastAPI and Uvicorn
- LangChain and Groq integration
- Authentication libraries (python-jose, passlib)
- Pydantic for data validation

### Frontend Files

#### `src/App.tsx`
Main application component:
- React Router setup
- Route definitions
- Private route protection
- Authentication state initialization

#### `src/pages/Login.tsx`
Login page component:
- Email/password form
- Form validation
- Error handling
- Navigation to registration

#### `src/pages/Register.tsx`
Registration page component:
- User registration form
- Password validation
- Account creation
- Auto-login after registration

#### `src/pages/Chat.tsx`
Main chat interface:
- Message display
- Chat input
- Real-time message updates
- Typing indicators
- Empty state with suggestions
- User actions (logout, clear chat)

#### `src/services/api.ts`
API client service:
- Axios HTTP client setup
- API endpoint methods
- Token management
- Request/response interceptors
- Error handling

#### `src/store/authStore.ts`
Authentication state management:
- User state
- Login/logout actions
- Registration
- Token persistence
- Error handling

#### `src/store/chatStore.ts`
Chat state management:
- Message history
- Send message action
- Loading states
- Conversation management

### Configuration Files

#### `backend/fly.toml`
Fly.io deployment configuration:
- App name and region
- Build configuration
- Environment variables
- HTTP service settings
- VM specifications

#### `frontend/vercel.json`
Vercel deployment configuration:
- Rewrite rules for SPA routing
- Ensures all routes serve index.html

#### `vite.config.ts`
Vite build tool configuration:
- React plugin setup
- Development server settings
- API proxy configuration

#### `tsconfig.json`
TypeScript compiler configuration:
- Target and module settings
- Strict type checking
- JSX configuration

### Documentation Files

#### `README.md`
Main project documentation:
- Project overview
- Features list
- Architecture diagram
- Tech stack details
- Quick start guide
- Deployment instructions

#### `docs/GETTING_STARTED.md`
Detailed setup guide:
- Prerequisites
- Step-by-step installation
- Configuration instructions
- Troubleshooting
- Development tips

#### `docs/DEPLOYMENT.md`
Production deployment guide:
- Fly.io deployment steps
- Vercel deployment steps
- Environment configuration
- Domain setup
- Monitoring
- Security checklist

#### `docs/API.md`
API reference documentation:
- All endpoints documented
- Request/response examples
- Authentication guide
- Error handling
- Testing examples

#### `docs/prd.md`
Product requirements document:
- Product vision
- Technical requirements
- Technology stack
- Feature specifications

### Development Scripts

#### `start-dev.sh` (Unix/Mac)
Automated development startup:
- Checks for required files
- Creates virtual environment if needed
- Installs dependencies
- Starts backend and frontend
- Provides status and logs
- Handles cleanup on exit

#### `start-dev.bat` (Windows)
Windows version of startup script:
- Same functionality as Unix version
- Windows-specific commands
- Separate terminal windows

## Key Features by File

### Authentication Flow
1. **Frontend**: `Login.tsx` → `authStore.ts` → `api.ts`
2. **Backend**: `main.py` (endpoint) → `auth.py` (logic)
3. **Token Storage**: `authStore.ts` (localStorage)

### Chat Flow
1. **Frontend**: `Chat.tsx` → `chatStore.ts` → `api.ts`
2. **Backend**: `main.py` (endpoint) → `agent.py` (AI logic)
3. **State**: `chatStore.ts` (conversation history)

### Deployment Flow
1. **Backend**: `fly.toml` → Fly.io → FastAPI app
2. **Frontend**: `vercel.json` → Vercel → React app
3. **Environment**: `.env` files → Configuration

## Technology Stack by File

### Backend Technologies
- **FastAPI** (`main.py`): Web framework
- **Groq** (`agent.py`): LLM provider
- **LangChain** (`agent.py`): AI orchestration
- **JWT** (`auth.py`): Authentication
- **Pydantic** (`models.py`, `config.py`): Data validation

### Frontend Technologies
- **React** (`.tsx` files): UI framework
- **TypeScript** (all `.ts/.tsx`): Type safety
- **Zustand** (`store/`): State management
- **Axios** (`api.ts`): HTTP client
- **Vite** (`vite.config.ts`): Build tool

### Deployment Technologies
- **Fly.io** (`fly.toml`): Backend hosting
- **Vercel** (`vercel.json`): Frontend hosting
- **Docker** (via Fly.io): Containerization

## Environment Variables

### Backend (`.env`)
```env
GROQ_API_KEY=xxx          # Required: Groq API key
SECRET_KEY=xxx            # Required: JWT secret
ALGORITHM=HS256           # Optional: JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30  # Optional: Token expiration
ALLOWED_ORIGINS=xxx       # Required: CORS origins
```

### Frontend (`.env`)
```env
VITE_API_URL=xxx          # Required: Backend API URL
```

## Getting Started

1. **Read First**: `README.md`
2. **Setup**: `docs/GETTING_STARTED.md`
3. **Deploy**: `docs/DEPLOYMENT.md`
4. **API Reference**: `docs/API.md`

## Development Workflow

1. **Start Development**:
   - Unix/Mac: `./start-dev.sh`
   - Windows: `start-dev.bat`

2. **Backend Development**:
   - Edit files in `backend/`
   - Server auto-reloads
   - Test at http://localhost:8000/docs

3. **Frontend Development**:
   - Edit files in `frontend/src/`
   - Vite auto-reloads
   - View at http://localhost:3000

4. **Testing**:
   - Backend: Use Swagger UI
   - Frontend: Use browser dev tools
   - End-to-end: Manual testing

## Adding New Features

### Backend
1. Define models in `models.py`
2. Add logic in appropriate module
3. Create endpoint in `main.py`
4. Update `docs/API.md`

### Frontend
1. Create/modify components in `src/pages/`
2. Add state management in `src/store/`
3. Update API service in `src/services/api.ts`
4. Add styling in `src/styles/`

## Notes

- **In-Memory Storage**: Current implementation uses in-memory user storage. Replace with a database for production.
- **Environment Variables**: Never commit `.env` files to version control.
- **API Keys**: Keep Groq API keys secure.
- **CORS**: Update `ALLOWED_ORIGINS` when deploying.
- **Secrets**: Generate strong `SECRET_KEY` for production.

## Maintenance

### Updating Dependencies

**Backend**:
```bash
cd backend
pip list --outdated
pip install --upgrade package_name
pip freeze > requirements.txt
```

**Frontend**:
```bash
cd frontend
npm outdated
npm update
# or
npm install package_name@latest
```

### Monitoring

- **Backend Logs**: `fly logs` or check Fly.io dashboard
- **Frontend Logs**: Vercel dashboard
- **Local Logs**: `backend.log` and `frontend.log` when using dev scripts

## Support

See individual README files in `backend/` and `frontend/` for component-specific documentation.
