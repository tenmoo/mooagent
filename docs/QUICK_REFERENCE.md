# MooAgent - Quick Reference

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your GROQ_API_KEY and SECRET_KEY
python main.py
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if needed
npm run dev
```

### Both at Once
```bash
./start-dev.sh      # Unix/Mac
start-dev.bat       # Windows
```

## 🔗 URLs

| Service | Development | Production |
|---------|------------|------------|
| Frontend | http://localhost:3000 | https://your-app.vercel.app |
| Backend API | http://localhost:8000 | https://your-app.fly.dev |
| API Docs | http://localhost:8000/docs | https://your-app.fly.dev/docs |
| Test MCP Server | http://localhost:3001 | N/A (local only) |

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | API info | ❌ |
| GET | `/health` | Health check | ❌ |
| POST | `/auth/register` | Register user | ❌ |
| POST | `/auth/login` | Login | ❌ |
| GET | `/auth/me` | Get user info | ✅ |
| POST | `/chat` | Send message | ✅ |
| GET | `/agent/info` | Agent info | ✅ |
| GET | `/agent/tools` | List available tools (including MCP) | ✅ |

## 🔐 Authentication

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"Hello!"}'
```

## 🛠️ Common Commands

### Backend

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run server | `python main.py` |
| Run with reload | `uvicorn main:app --reload` |
| Generate secret | `openssl rand -hex 32` |
| View logs (prod) | `fly logs` |
| Deploy | `fly deploy` |

### Frontend

| Task | Command |
|------|---------|
| Install deps | `npm install` |
| Run dev server | `npm run dev` |
| Build | `npm run build` |
| Preview build | `npm run preview` |
| Lint | `npm run lint` |
| Deploy | `vercel --prod` |

### Test MCP Server

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run server | `python mcp_test_server.py` |
| Test endpoint | `curl http://localhost:3001/tools/list` |

## 📁 Project Structure

```
mooagent/
├── backend/          # FastAPI + Groq + LangChain
│   ├── main.py       # API routes
│   ├── agent.py      # AI agent
│   ├── auth.py       # Authentication
│   └── models.py     # Data models
├── frontend/         # React + TypeScript + Vite
│   └── src/
│       ├── pages/    # UI pages
│       ├── services/ # API client
│       └── store/    # State management
└── docs/            # Documentation
```

## 🔧 Environment Variables

### Backend `.env`
```env
GROQ_API_KEY=your_key
SECRET_KEY=your_secret
ALLOWED_ORIGINS=http://localhost:3000
MCP_SERVER_URL=http://localhost:3001  # Optional
```

### Frontend `.env`
```env
VITE_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Backend to Fly.io
```bash
cd backend
fly launch
fly secrets set GROQ_API_KEY=xxx SECRET_KEY=xxx
fly deploy
```

### Frontend to Vercel
```bash
cd frontend
vercel --prod
# Set VITE_API_URL in Vercel dashboard
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -ti:8000 \| xargs kill -9` |
| Port 3000 in use | `lsof -ti:3000 \| xargs kill -9` |
| CORS error | Check ALLOWED_ORIGINS in backend .env |
| 401 Unauthorized | Login again or check token |
| Module not found | Reinstall dependencies |

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](../README.md) | Project overview |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Detailed setup |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |
| [API.md](API.md) | API reference |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | File structure |

## 🔑 Key Technologies

- **Backend**: FastAPI, Groq (OpenAI GPT-OSS & Meta LLaMA), LangChain, JWT
- **Frontend**: React, TypeScript, Zustand, Axios, Vite, react-markdown
- **Deployment**: Fly.io (backend), Vercel (frontend)

## 💡 Tips

- Use Swagger UI for API testing: http://localhost:8000/docs
- Check browser console for frontend errors
- Use `fly logs` for backend debugging
- Keep dependencies updated
- Never commit `.env` files

## 🆘 Getting Help

1. Check documentation in `docs/`
2. Review error messages in logs
3. Test API endpoints in Swagger UI
4. Open issue on GitHub

---

**Quick Links**: [Main README](../README.md) | [Setup Guide](GETTING_STARTED.md) | [Deploy Guide](DEPLOYMENT.md) | [API Docs](API.md)
