# MooAgent - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                         (Browser - localhost:3000)                          │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 │ HTTPS/HTTP
                                 │
┌────────────────────────────────▼────────────────────────────────────────────┐
│                            FRONTEND (Vercel)                                 │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                        React Application                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │    │
│  │  │  Login.tsx   │  │ Register.tsx │  │   Chat.tsx   │            │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │    │
│  │         │                  │                   │                   │    │
│  │         └──────────────────┴───────────────────┘                   │    │
│  │                             │                                       │    │
│  │                   ┌─────────▼──────────┐                           │    │
│  │                   │   State Stores     │                           │    │
│  │                   │  ┌──────────────┐  │                           │    │
│  │                   │  │  authStore   │  │                           │    │
│  │                   │  │  chatStore   │  │                           │    │
│  │                   │  └──────────────┘  │                           │    │
│  │                   └─────────┬──────────┘                           │    │
│  │                             │                                       │    │
│  │                   ┌─────────▼──────────┐                           │    │
│  │                   │    API Service     │                           │    │
│  │                   │     (Axios)        │                           │    │
│  │                   └─────────┬──────────┘                           │    │
│  └─────────────────────────────┼────────────────────────────────────────┘  │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │
                                 │ REST API (JSON)
                                 │ Authorization: Bearer <JWT>
                                 │
┌────────────────────────────────▼────────────────────────────────────────────┐
│                            BACKEND (Fly.io)                                  │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                       FastAPI Application                           │    │
│  │  ┌──────────────────────────────────────────────────────────┐     │    │
│  │  │                    API Endpoints                          │     │    │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │     │    │
│  │  │  │  /auth/* │  │  /chat   │  │ /agent/* │  │ /health │ │     │    │
│  │  │  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │     │    │
│  │  └───────┬──────────────┬─────────────────────────────────┘     │    │
│  │          │              │                                         │    │
│  │  ┌───────▼──────┐  ┌────▼─────────┐                              │    │
│  │  │   auth.py    │  │   agent.py   │                              │    │
│  │  │              │  │              │                              │    │
│  │  │ • JWT Token  │  │ • LangChain  │                              │    │
│  │  │ • Password   │  │ • Agent      │───────┐                      │    │
│  │  │   Hashing    │  │ • Tools      │       │                      │    │
│  │  │ • User Mgmt  │  │              │       │                      │    │
│  │  └──────────────┘  └────┬─────────┘       │                      │    │
│  │                          │          ┌──────▼──────┐              │    │
│  │                ┌─────────▼──────────┤ mcp_agent.py│              │    │
│  │                │    models.py       │ • MCP Tools │              │    │
│  │                │  (Pydantic Models) │ • Remote    │              │    │
│  │                └────────────────────┤   Servers   │              │    │
│  │                                     └─────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 │ HTTPS API
                                 │
┌────────────────────────────────▼────────────────────────────────────────────┐
│                          GROQ API (Multi-Model)                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                OpenAI GPT-OSS & Meta LLaMA Models                   │    │
│  │                                                                      │    │
│  │  • GPT-OSS 120B (500 t/s) - Flagship model                         │    │
│  │  • GPT-OSS 20B (1000 t/s) - Fast model                             │    │
│  │  • LLaMA 3.3 70B (280 t/s) - Latest Meta model                     │    │
│  │  • LLaMA 3.1 8B (560 t/s) - Fastest model                          │    │
│  │  • Natural Language Understanding                                   │    │
│  │  • Conversational AI                                                │    │
│  │  • Context-Aware Responses                                          │    │
│  │  • Ultra-Fast Inference (Groq infrastructure)                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Authentication Flow
```
User (Browser)
    │
    │ 1. Enter credentials
    ▼
Login.tsx
    │
    │ 2. Submit form
    ▼
authStore.ts
    │
    │ 3. Call API
    ▼
api.ts (Axios)
    │
    │ 4. POST /auth/login
    ▼
FastAPI (main.py)
    │
    │ 5. Validate credentials
    ▼
auth.py
    │
    │ 6. Generate JWT
    ▼
Response with Token
    │
    │ 7. Store token
    ▼
localStorage
    │
    │ 8. Redirect to Chat
    ▼
Chat Interface
```

### 2. Chat Flow
```
User (Browser)
    │
    │ 1. Type message
    ▼
Chat.tsx
    │
    │ 2. Update UI
    ▼
chatStore.ts
    │
    │ 3. Send to API
    ▼
api.ts (Axios)
    │
    │ 4. POST /chat + JWT
    ▼
FastAPI (main.py)
    │
    │ 5. Verify JWT
    ▼
auth.py (middleware)
    │
    │ 6. Forward to agent
    ▼
agent.py (MooAgent)
    │
    │ 7. Process with LangChain
    ▼
Groq API (GPT-OSS or LLaMA)
    │
    │ 8. Generate response
    ▼
agent.py
    │
    │ 9. Return response
    ▼
FastAPI
    │
    │ 10. Send to frontend
    ▼
chatStore.ts
    │
    │ 11. Update messages
    ▼
Chat.tsx
    │
    │ 12. Display message
    ▼
User sees response
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Components                      │
│                                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Pages   │───▶│  Stores  │───▶│ Services │              │
│  │          │    │          │    │          │              │
│  │ • Login  │    │ • Auth   │    │ • API    │              │
│  │ • Reg    │    │ • Chat   │    │          │              │
│  │ • Chat   │    │          │    │          │              │
│  └──────────┘    └──────────┘    └────┬─────┘              │
│                                        │                     │
└────────────────────────────────────────┼─────────────────────┘
                                         │
                                         │ HTTP/REST
                                         │
┌────────────────────────────────────────┼─────────────────────┐
│                     Backend Components  │                     │
│                                         │                     │
│  ┌─────────┐    ┌──────────┐    ┌─────▼─────┐              │
│  │ Models  │◀───│   Auth   │◀───│   Main    │              │
│  │         │    │          │    │  (FastAPI) │              │
│  │ • User  │    │ • JWT    │    │           │              │
│  │ • Chat  │    │ • Hash   │    │ • Routes  │              │
│  │ • Token │    │          │    │ • CORS    │              │
│  └─────────┘    └──────────┘    └─────┬─────┘              │
│                                        │                     │
│                                  ┌─────▼─────┐              │
│                                  │   Agent   │              │
│                                  │           │              │
│                                  │ • Chain   │              │
│                                  │ • Tools   │              │
│                                  └─────┬─────┘              │
│                                        │                     │
└────────────────────────────────────────┼─────────────────────┘
                                         │
                                         │ API Call
                                         │
┌────────────────────────────────────────▼─────────────────────┐
│                        External Services                      │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Groq API (Multi-Model Infrastructure)       │   │
│  │                                                       │   │
│  │  • OpenAI GPT-OSS 120B & 20B models                 │   │
│  │  • Meta LLaMA 3.3 70B & 3.1 8B models               │   │
│  │  • Ultra-fast inference (280-1000 t/s)              │   │
│  │  • Large context window (131K tokens)               │   │
│  │  • High-quality responses                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Technology Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  • React Components (TSX)                                    │
│  • CSS Styling (Dark Theme)                                  │
│  • User Interactions                                         │
│  • Markdown Rendering (react-markdown + remark-gfm)          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    State Management Layer                    │
│  • Zustand Stores                                            │
│  • Local State                                               │
│  • Client-side Logic                                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    API Communication Layer                   │
│  • Axios HTTP Client                                         │
│  • Request/Response Interceptors                             │
│  • Token Management                                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ REST API
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    API Gateway Layer                         │
│  • FastAPI Routes                                            │
│  • Request Validation                                        │
│  • CORS Handling                                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Business Logic Layer                      │
│  • Authentication (JWT)                                      │
│  • User Management                                           │
│  • Agent Orchestration                                       │
│  • MCP Sub-Agent (Remote Tools)                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    AI/ML Layer                               │
│  • LangChain Framework                                       │
│  • Agent Tools                                               │
│  • Conversation Memory                                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    External AI Services                      │
│  • Groq API                                                  │
│  • OpenAI GPT-OSS 120B & 20B (Groq-hosted)                  │
│  • Meta LLaMA 3.3 70B & 3.1 8B (Groq-hosted)                │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└────────────┬────────────────────────────┬───────────────────┘
             │                            │
             │                            │
    ┌────────▼────────┐          ┌───────▼────────┐
    │  Vercel CDN     │          │   Fly.io       │
    │  (Frontend)     │          │   (Backend)    │
    │                 │          │                │
    │ • React App     │          │ • FastAPI      │
    │ • Static Files  │◀────────▶│ • Docker       │
    │ • Edge Network  │   API    │ • Container    │
    └─────────────────┘  Calls   └───────┬────────┘
                                          │
                                          │
                                  ┌───────▼────────┐
                                  │   Groq API     │
                                  │   (External)   │
                                  │                │
                                  │ • GPT-OSS 120B │
                                  │ • GPT-OSS 20B  │
                                  │ • LLaMA 3.3 70B│
                                  │ • LLaMA 3.1 8B │
                                  └────────────────┘
```

## Security Flow

```
1. User Registration
   ────────────────────────────────────────
   Password (Plain) ──▶ Bcrypt Hash ──▶ Store

2. User Login
   ────────────────────────────────────────
   Password (Plain) ──▶ Verify Hash ──▶ Generate JWT ──▶ Send Token

3. Authenticated Request
   ────────────────────────────────────────
   Request + JWT ──▶ Verify JWT ──▶ Extract User ──▶ Process ──▶ Response

4. CORS Protection
   ────────────────────────────────────────
   Origin Check ──▶ Allowed? ──▶ Yes: Allow / No: Block
```

## File Structure Mapping

```
Frontend                        Backend
────────                        ───────
src/pages/Login.tsx      ──▶   /auth/login
src/pages/Register.tsx   ──▶   /auth/register
src/pages/Chat.tsx       ──▶   /chat, /agent/tools, /agent/models
src/services/api.ts      ──▶   All endpoints
src/store/authStore.ts   ──▶   Auth state
src/store/chatStore.ts   ──▶   Chat state + model selection

                         Backend Structure
                         ─────────────────
                         main.py        ─ API routes
                         auth.py        ─ Auth logic
                         agent.py       ─ AI agent
                         mcp_agent.py   ─ MCP integration
                         models.py      ─ Data models
                         config.py      ─ Settings
```

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Scalable structure
- ✅ Secure authentication
- ✅ Fast AI responses
- ✅ Modern deployment (Edge + Containers)
- ✅ Rich markdown rendering with GFM
- ✅ Model selection and switching
- ✅ MCP integration for extensibility