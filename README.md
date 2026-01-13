# MooAgent - AI Personal Assistant

An AI-powered personal assistant that helps with your daily work, built with modern technologies.

![MooAgent](https://img.shields.io/badge/AI-Powered-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Frontend](https://img.shields.io/badge/Frontend-React-blue)
![LLM](https://img.shields.io/badge/LLM-Groq-orange)

## 🚀 Features

- 🤖 **AI-Powered Conversations**: Intelligent responses powered by Groq LLaMA 3
- 🔌 **MCP Integration**: Connect to remote tools via Model Context Protocol
- 🛠️ **Tool Discovery**: View available tools directly in the chat interface
- 🧪 **Test MCP Server**: Includes ready-to-use test server with 4 example tools
- 🔐 **Secure Authentication**: JWT-based authentication with OAuth 2.0 pattern
- 💬 **Real-time Chat**: Beautiful, responsive chat interface
- 🎨 **Modern UI**: Dark theme with smooth animations
- 📱 **Responsive Design**: Works seamlessly on all devices
- 🚀 **High Performance**: Built with FastAPI and React for optimal speed

## 🏗️ Architecture

```
mooagent/
├── backend/          # FastAPI backend
│   ├── main.py       # API routes and FastAPI app
│   ├── agent.py      # AI agent implementation
│   ├── mcp_agent.py  # MCP sub-agent for remote tools
│   ├── auth.py       # Authentication logic
│   ├── models.py     # Pydantic models
│   └── config.py     # Configuration
│
├── frontend/         # React TypeScript frontend
│   ├── src/
│   │   ├── pages/    # Page components
│   │   ├── services/ # API services
│   │   ├── store/    # State management
│   │   └── styles/   # CSS styles
│   └── public/       # Static assets
│
├── test-mcp-server/ # Test MCP server with example tools
│   ├── mcp_test_server.py
│   └── requirements.txt
│
└── docs/            # Documentation
    └── prd.md       # Product requirements
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **AI/LLM**: Groq (LLaMA 3 70B)
- **AI Framework**: LangChain
- **Authentication**: JWT with OAuth 2.0
- **Deployment**: Fly.io
- **Language**: Python 3.9+

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router
- **Deployment**: Vercel

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Groq API key ([Get one here](https://console.groq.com))

## 🚀 Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```env
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key  # Generate with: openssl rand -hex 32
ALLOWED_ORIGINS=http://localhost:3000
```

6. Start the backend server:
```bash
python main.py
```

Backend will be running at http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`:
```env
VITE_API_URL=http://localhost:8000
```

5. Start the development server:
```bash
npm run dev
```

Frontend will be running at http://localhost:3000

## 🧪 Testing MCP Integration

MooAgent includes a test MCP server with example tools. To try it:

### Start the Test MCP Server

```bash
cd test-mcp-server
pip install -r requirements.txt
python mcp_test_server.py
```

Server will run on http://localhost:3001 with 4 tools:
- **calculator** - Basic math operations
- **weather** - Simulated weather data
- **time** - Current time in any timezone
- **uuid** - Generate random UUIDs

### Configure MooAgent to Use It

Edit `backend/.env`:
```env
MCP_SERVER_URL=http://localhost:3001
```

Restart backend and try in chat:
- "What's 25 + 17?"
- "What's the weather in Tokyo?"
- "Generate a UUID"
- Click **"Show Tools"** to see all available tools!

## 📚 API Documentation

Once the backend is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info

#### Chat
- `POST /chat` - Send message to AI agent
- `GET /agent/info` - Get agent information

## 🚀 Deployment

### Deploy Backend to Fly.io

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to Fly:
```bash
fly auth login
```

3. Navigate to backend directory and launch:
```bash
cd backend
fly launch
```

4. Set secrets:
```bash
fly secrets set GROQ_API_KEY=your_groq_api_key
fly secrets set SECRET_KEY=your_secret_key
fly secrets set ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

5. Deploy:
```bash
fly deploy
```

### Deploy Frontend to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Navigate to frontend directory and deploy:
```bash
cd frontend
vercel --prod
```

4. Set environment variable in Vercel dashboard:
   - `VITE_API_URL`: Your backend URL (e.g., https://your-app.fly.dev)

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for secure authentication
- CORS configured for allowed origins
- Environment variables for sensitive data
- HTTPS enforced in production

## 🧪 Development

### Backend Development

Run with auto-reload:
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Development

Run with hot-reload:
```bash
cd frontend
npm run dev
```

### Linting

Frontend:
```bash
cd frontend
npm run lint
```

## 📝 Environment Variables

### Backend (.env)
```env
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=MooAgent
APP_VERSION=1.0.0
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://react.dev/) - UI library
- [Groq](https://groq.com/) - Fast AI inference
- [LangChain](https://www.langchain.com/) - LLM framework
- [Fly.io](https://fly.io/) - Backend deployment
- [Vercel](https://vercel.com/) - Frontend deployment

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, React, and Groq**
