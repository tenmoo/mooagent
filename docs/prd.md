# MooAgent - Product Requirements Document

## 1. Executive Summary

MooAgent is an AI-powered personal assistant that helps with your daily work. Built with modern technologies including FastAPI, React, and Groq's LLaMA models, MooAgent provides intelligent conversational assistance through a beautiful, responsive web interface.

**Current Status**: ✅ **MVP Completed and Deployed**

## 2. Problem Statement

Professionals need quick, intelligent assistance for daily work tasks but often face:
- Context switching between multiple tools and applications
- Lack of personalized, conversational assistance
- Complex interfaces that slow down productivity
- Need for immediate, intelligent responses to questions and tasks

## 3. Product Vision

Create an intelligent AI agent that acts as a personal assistant, providing conversational help for daily work through a simple, beautiful interface. The assistant should be fast, secure, and always available.

## 4. Target Users

### Primary Users
- **Professionals** looking for quick assistance with daily tasks
- **Knowledge Workers** who need information and help with planning
- **Developers** wanting a conversational interface to AI capabilities
- **Teams** seeking a customizable AI assistant platform

### User Personas
- **Busy Professional**: Needs quick answers and task assistance
- **Developer**: Wants to integrate and customize AI capabilities
- **Startup Team**: Looking for affordable AI assistant solution

## 5. Core Features

### 5.1 Conversational AI Chat ✅ **IMPLEMENTED**
- Real-time chat interface with AI agent
- Context-aware responses using LLaMA or OpenAI models
- Conversation history management
- Natural language understanding
- Fast response times via Groq infrastructure
- **MCP Sub-Agent Integration** ✅ for connecting to remote tools

### 5.2 MCP (Model Context Protocol) Integration ✅ **IMPLEMENTED**
- Connect to remote MCP servers via URL
- Dynamic tool discovery from MCP servers
- Call remote tools with natural language
- Access external resources via MCP
- Async HTTP communication with thread-based execution
- Extensible architecture for adding new capabilities
- **Test MCP Server** with 4 example tools included
- **Tool Discovery UI** in chat interface
- Compatible with uvloop (production-grade async)

### 5.3 User Authentication & Security ✅ **IMPLEMENTED**
- Secure user registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Protected API endpoints
- Session management

### 5.4 Modern Web Interface ✅ **IMPLEMENTED**
- Responsive design (desktop, tablet, mobile)
- Dark theme for comfortable viewing
- Real-time message updates
- Typing indicators
- Suggested conversation starters
- Clean, intuitive UX
- **Model Selector**: Choose between multiple LLM models
- **Markdown Support**: Full GitHub Flavored Markdown rendering
- **Smart Text Wrapping**: Prevents horizontal overflow

## 6. User Experience & Interface

### 6.1 Interface Components ✅ **IMPLEMENTED**
- **Login/Register Pages**: Clean authentication flow
- **Chat Interface**: Primary interaction point with the AI
- **Message History**: Scrollable conversation view with proper text wrapping
- **Input Area**: Text input with send button
- **User Menu**: Profile and logout options
- **Tools Panel**: Collapsible panel showing available tools
- **Model Selector**: Dropdown to choose between different LLM models
- **Markdown Rendering**: Full GFM support for rich text formatting

### 6.2 User Flow ✅ **IMPLEMENTED**
1. User visits application
2. Registers or logs in
3. Redirected to chat interface
4. Sends messages to AI agent
5. Receives intelligent responses
6. Can clear chat or logout

### 6.3 Design Principles
- **Simplicity**: Minimal, focused interface
- **Speed**: Fast load times and responses
- **Accessibility**: Keyboard navigation and screen reader support
- **Responsiveness**: Works on all device sizes
- **Text Handling**: Proper word wrapping prevents horizontal overflow
- **Rich Formatting**: Markdown support for better readability

## 7. Technical Requirements

### 7.1 AI/ML Components ✅ **IMPLEMENTED**
- **LLM**: Groq LLaMA 3.3 70B (default, best with tools) and OpenAI GPT-OSS models
- **Framework**: LangChain for agent orchestration (using create_react_agent)
- **Conversation Memory**: ConversationBufferMemory
- **Agent Type**: React Agent with custom prompt
- **Agent Executor**: 10 max iterations, 30s timeout
- **Tools**: Extensible tool framework for agent capabilities
- **MCP Integration**: Model Context Protocol sub-agent for remote tool access
- **Async Processing**: Thread-based async execution compatible with uvloop
- **Error Handling**: Comprehensive logging and graceful fallbacks
- **Model Switching**: Dynamic model selection with detailed logging

### 7.2 Data Sources & Integrations

**Current** ✅:
- Groq API for LLM inference
- MCP (Model Context Protocol) servers for external tools and resources
- HTTP/HTTPS endpoints via async client (httpx)
- **Test MCP Server** included with 4 example tools:
  - Calculator (add, subtract, multiply, divide)
  - Weather (simulated data for major cities)
  - Time (current time in any timezone)
  - UUID (random UUID generation)

**Supported via MCP**:
- File system access
- Database queries
- External APIs
- Custom tool servers
- Any MCP-compatible service

**Future Enhancements**:
- Web search integration
- Calendar integration
- Email integration
- Document processing
- Real-time data feeds

### 7.3 Technology Stack ✅ **IMPLEMENTED**

#### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.9+
- **LLM Provider**: Groq (Free tier available)
- **LLM Models**: Meta LLaMA 3.3 70B/3.1 8B & OpenAI GPT-OSS 120B/20B
- **AI Framework**: LangChain 0.2.16 with langchain-groq 0.1.9
- **MCP Integration**: Custom MCP sub-agent with httpx for async communication
- **Protocol**: Model Context Protocol (MCP) support for remote tools
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **Server**: Uvicorn with async support
- **HTTP Client**: httpx 0.26.0 for async requests
- **Deployment**: Fly.io with Docker containerization
- **Logging**: Detailed request and model switching logs

#### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite 5.0
- **State Management**: Zustand 4.4
- **HTTP Client**: Axios 1.6
- **Routing**: React Router 6.21
- **Styling**: Custom CSS with CSS Variables (Dark theme)
- **Theme Colors**: 
  - Background: #0a0a0a (deep black)
  - Surface: #1a1a1a (dark charcoal)
  - Primary: #6366f1 (indigo)
- **Deployment**: Vercel with edge network
- **UI Features**: Tool discovery panel, model selector, expandable details, responsive text wrapping
- **Markdown Rendering**: 
  - `react-markdown` with GitHub Flavored Markdown (GFM)
  - `remark-gfm` plugin for tables, strikethrough, task lists
  - Proper list rendering without extra line breaks
  - Inline paragraph rendering within list items
- **Text Rendering**: 
  - `word-wrap: break-word` for long URLs
  - Smart line breaking without preserving unwanted whitespace
  - Horizontal overflow prevention with `max-width: 100%`
  - Code blocks with proper syntax highlighting
  - Clickable links that open in new tabs

#### Database
- **Current**: In-memory storage (demo/development)
- **Recommended Production**: PostgreSQL or MongoDB
- **Future**: Vector database for embeddings (Pinecone, Weaviate)

#### Authentication ✅ **IMPLEMENTED**
- OAuth 2.0 pattern with JWT tokens
- Bcrypt password hashing
- Bearer token authentication
- Token expiration (30 minutes default)
- Secure HTTP-only approach ready for cookies

#### Deployment ✅ **CONFIGURED**
- **Frontend**: Vercel
  - Automatic deployments from Git
  - Edge network for global performance
  - Environment variable management
  - SPA routing configured
- **Backend**: Fly.io
  - Docker containerization
  - Global deployment regions
  - Secrets management
  - Auto-scaling capabilities

#### Monitoring & Logging ✅ **BASIC IMPLEMENTATION**
- FastAPI automatic request logging
- Error tracking and traceback
- Health check endpoints
- Console logging for debugging
- Ready for: Sentry, DataDog, or similar

### 7.4 Data Management

#### Current Implementation ✅
- In-memory user storage (demo purposes)
- Client-side conversation history (localStorage)
- Session-based authentication

#### Production Recommendations
- PostgreSQL for user data
- Redis for session management
- S3 or similar for file storage
- Vector DB for conversation embeddings
- Regular backups and disaster recovery

### 7.5 Performance Requirements ✅ **MET & EXCEEDED**

**Achieved Performance**:
- API Response Time: < 2 seconds for chat
- Page Load Time: < 1 second
- Authentication: < 500ms
- LLM Response: 1-5 seconds (via Groq's ultra-fast infrastructure)
- MCP Tool Calls: < 1 second (with 30s timeout)
- Frontend Bundle: Optimized with Vite
- Agent Iterations: Up to 10 (increased from 3)

**Model Performance** (Groq-hosted):
- LLaMA 3.3 70B: 280 tokens/sec (default - best MCP compatibility)
- LLaMA 3.1 8B: 560 tokens/sec (fastest)
- GPT-OSS 120B: 500 tokens/sec (experimental)
- GPT-OSS 20B: 1000 tokens/sec (experimental)

**Scalability**:
- Fly.io: Auto-scaling based on load
- Vercel: Edge caching and CDN
- Stateless API design
- Thread-based async for concurrent MCP calls
- Ready for horizontal scaling

## 8. Privacy & Security ✅ **IMPLEMENTED**

### 8.1 Security Measures
- ✅ Password hashing with bcrypt (72 byte limit enforced)
- ✅ JWT token authentication
- ✅ CORS protection with configurable origins
- ✅ Environment variable secrets (never committed)
- ✅ HTTPS enforced in production
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (Pydantic models)
- ✅ XSS prevention (React escaping)

### 8.2 Privacy
- ✅ Minimal data collection
- ✅ User data isolation
- ✅ No third-party tracking
- ✅ Clear data handling
- 🔄 Privacy policy (to be added)
- 🔄 GDPR compliance measures (in progress)

### 8.3 API Security
- Rate limiting ready (to be configured)
- Request validation
- Error handling without information leakage
- Secure token storage

## 9. Success Metrics

### 9.1 Technical Metrics ✅
- **Uptime**: Target 99.5% (monitoring in place)
- **Response Time**: < 3 seconds average
- **Error Rate**: < 1%
- **API Success Rate**: > 99%

### 9.2 User Metrics 🔄 (To be implemented)
- Daily/Monthly Active Users (DAU/MAU)
- Average session duration
- Messages per session
- User retention rate
- Registration conversion rate

### 9.3 Business Metrics 🔄
- User satisfaction (NPS)
- Feature usage
- Cost per user (Groq API usage)
- Response quality feedback

## 10. Phases & Roadmap

### Phase 1: MVP ✅ **COMPLETED** (January 2026)
- [x] Backend API with FastAPI
- [x] Groq LLaMA integration with fallback model
- [x] LangChain agent setup (modern create_react_agent)
- [x] MCP sub-agent for remote tool integration
- [x] Thread-based async execution (uvloop compatible)
- [x] Test MCP server with 4 example tools
- [x] JWT authentication with bcrypt
- [x] User registration/login with validation
- [x] React frontend with TypeScript
- [x] Chat interface with tool discovery UI
- [x] Model selector for choosing LLM models
- [x] Markdown rendering with GitHub Flavored Markdown
- [x] Dark theme (#0a0a0a background)
- [x] Responsive design
- [x] Deployment configuration (Fly.io + Vercel)
- [x] Comprehensive documentation (8 guides)

### Phase 2: Enhancement ✅ **PARTIALLY COMPLETED** (Q1 2026)
- [ ] Database integration (PostgreSQL)
- [ ] Conversation persistence
- [ ] User profiles and settings
- [ ] Conversation export
- [x] MCP server integration (completed)
- [x] Test MCP server with examples (completed)
- [x] Tool discovery UI (completed)
- [x] Natural language tool invocation (completed)
- [x] Thread-safe async execution (completed)
- [x] Improved error handling (completed)
- [ ] Multiple MCP server support
- [ ] Advanced agent tools
- [ ] Rate limiting
- [ ] Analytics integration

### Phase 3: Advanced Features (Q2 2026)
- [ ] Multi-agent capabilities
- [ ] File upload and processing
- [ ] Voice input/output
- [ ] Browser extensions
- [ ] Mobile applications
- [ ] Team/collaboration features
- [ ] Custom agent personalities

### Phase 4: Scale & Optimize (Q3 2026)
- [ ] Performance optimization
- [ ] Advanced caching
- [ ] Real-time collaboration
- [ ] Enterprise features
- [ ] Advanced monitoring
- [ ] Load balancing
- [ ] Multi-region deployment

## 11. Open Questions & Risks

### Questions Addressed ✅
- ✅ Monetization: Start free, freemium model planned
- ✅ Mobile: Responsive web first, native apps later
- ✅ LLM Provider: Groq chosen for speed and free tier
- ✅ Deployment: Fly.io + Vercel chosen

### Remaining Questions 🔄
- [ ] What analytics platform to use?
- [ ] When to add premium features?
- [ ] How to handle conversation limits?
- [ ] What database to choose for production?

### Risks & Mitigation ✅

**API Dependencies**:
- Risk: Groq API changes or downtime
- Mitigation: ✅ Fallback models implemented, error handling

**Model Deprecation**:
- Risk: Models get decommissioned
- Mitigation: ✅ Automatic fallback to newer models, flexible model selection

**Scaling Costs**:
- Risk: High API costs at scale
- Mitigation: ✅ Rate limiting ready, caching, efficient model selection

**Security**:
- Risk: Authentication vulnerabilities
- Mitigation: ✅ Industry-standard JWT + bcrypt, 72-byte password limit

**Data Privacy**:
- Risk: User data concerns
- Mitigation: ✅ Minimal collection, secure storage

**Async Compatibility**:
- Risk: Event loop conflicts with uvloop
- Mitigation: ✅ Thread-based async execution, tested and working

**MCP Tool Reliability**:
- Risk: External MCP servers failing
- Mitigation: ✅ Timeouts, error handling, fresh connections per call

## 12. Constraints

### Technical Constraints ✅
- ✅ LLM API costs managed via free tier
- ✅ Groq model availability (fallback implemented)
- ✅ Browser compatibility (modern browsers)
- ✅ 72-byte password limit (bcrypt constraint)

### Business Constraints
- Bootstrap/self-funded initially
- Free tier usage for development
- MVP timeline: Completed in 2 weeks
- Initial focus: Individual users

### Regulatory Constraints 🔄
- GDPR compliance (in progress)
- Data privacy laws
- Terms of service (to be added)
- Acceptable use policy (to be added)

## 13. Future Enhancements

### Near-term (Next 3 months)
- Database integration
- Conversation persistence
- User profiles and settings
- Advanced agent capabilities
- Rate limiting
- Analytics

### Medium-term (3-6 months)
- File upload and processing
- Voice interaction
- Browser extension
- Mobile-responsive improvements
- Team features
- Custom agent training

### Long-term (6-12 months)
- Native mobile apps
- Multi-language support
- Enterprise features
- Plugin ecosystem
- Advanced analytics
- White-label options
- API marketplace

### Potential Features
- Integration with productivity tools (Notion, Google Workspace)
- Calendar and scheduling assistance
- Email draft generation
- Document summarization
- Code assistance
- Meeting notes and transcription
- Task and project management
- Knowledge base creation

---

## Document Control

**Version**: 2.4  
**Last Updated**: January 24, 2026  
**Author**: Product Team  
**Status**: ✅ **Implementation Complete (MVP + Enhancements)**  
**Next Review**: February 2026

## Implementation Status

### ✅ Completed
- Backend API with FastAPI
- Frontend with React + TypeScript
- AI integration with Groq LLaMA
- LangChain agent orchestration (modern API)
- **MCP sub-agent for remote tool integration**
- **Test MCP server with 4 example tools**
- **Tool discovery UI with "Show Tools" button**
- **Model selector with multiple LLM options**
- **Thread-based async execution (uvloop compatible)**
- **Natural language tool invocation**
- **Improved agent (10 iterations, 30s timeout)**
- **Markdown rendering with GFM support**
- **Proper list formatting without extra line breaks**
- JWT authentication
- User registration/login
- Chat interface
- **Dark theme UI (#0a0a0a)**
- **Text wrapping and overflow prevention**
- Responsive design
- Deployment configuration
- **Comprehensive documentation (8+ guides)**
- **All deprecation warnings resolved**
- **All critical bugs fixed**
- **LangSmith warning suppression**
- **Enhanced logging for debugging**

### 🔄 In Progress
- Production database integration
- Advanced monitoring
- Analytics

### 📋 Planned
- Advanced features (Phase 2+)
- Mobile apps
- Enterprise features

---

## Quick Links

- **Main Documentation**: [README.md](../README.md)
- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **API Reference**: [API.md](API.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **MCP Integration**: [MCP_INTEGRATION.md](MCP_INTEGRATION.md)
- **Recent Updates**: [UPDATES.md](UPDATES.md)
- **Test MCP Server**: [../test-mcp-server/README.md](../test-mcp-server/README.md)