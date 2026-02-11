# Getting Started with MooAgent

This guide will help you get MooAgent up and running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: [Download here](https://www.python.org/downloads/)
- **Node.js 18+**: [Download here](https://nodejs.org/)
- **Git**: [Download here](https://git-scm.com/)

You'll also need:
- A Groq API key (free): [Get one here](https://console.groq.com/)

## Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd mooagent
```

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Generate a secret key:
```bash
openssl rand -hex 32
```

3. Edit `.env` and add your configuration:
```env
GROQ_API_KEY=your_actual_groq_api_key
SECRET_KEY=your_generated_secret_key
ALLOWED_ORIGINS=http://localhost:3000

# Optional: MCP Server Integration
MCP_SERVER_URL=http://localhost:3001
```

### 2.5 Start Backend Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is now running! Visit http://localhost:8000/docs to see the API documentation.

## Step 3: Frontend Setup

Open a **new terminal window** (keep the backend running).

### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.2 Install Dependencies

```bash
npm install
```

This may take a few minutes on first run.

### 3.3 Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. The default configuration should work:
```env
VITE_API_URL=http://localhost:8000
```

### 3.4 Start Frontend Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
```

✅ Frontend is now running! Visit http://localhost:3000

## Step 4: Create Your First Account

1. Open http://localhost:3000 in your browser
2. Click "Sign Up" to create a new account
3. Enter your email and password (minimum 8 characters)
4. Click "Sign Up"

You'll be automatically logged in and redirected to the chat interface.

## Step 5: (Optional) Test MCP Integration

MooAgent includes a test MCP server with example tools.

### 5.1 Start the Test MCP Server

Open a **third terminal window**:

```bash
cd test-mcp-server
pip install -r requirements.txt
python mcp_test_server.py
```

You should see:
```
🚀 Starting MCP Test Server...
📍 Server will be available at: http://localhost:3001
🛠️  Available tools: calculator, weather, time, uuid
```

### 5.2 Configure MooAgent

Edit `backend/.env` and add:
```env
MCP_SERVER_URL=http://localhost:3001
```

### 5.3 Restart Backend

In the backend terminal (Ctrl+C to stop, then):
```bash
python main.py
```

You should see:
```
✅ MCP sub-agent initialized with server: http://localhost:3001
```

### 5.4 Try MCP Tools

In the chat interface:
- Click **"Show Tools"** to see all available tools
- Try: "What's 25 + 17?"
- Try: "What's the weather in Tokyo?"
- Try: "Generate a UUID"

---

## Step 6: Start Chatting!

Try these example prompts:
- "What can you help me with?"
- "Help me plan my day"
- "Tell me about yourself"

## Troubleshooting

### Backend Issues

**Error: "No module named 'fastapi'"**
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt` again

**Error: "Groq API key not found"**
- Check that you've created a `.env` file in the backend directory
- Verify your `GROQ_API_KEY` is set correctly
- Make sure there are no quotes around the key

**Port 8000 already in use:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Error: "Cannot find module"**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Port 3000 already in use:**
- Vite will automatically suggest an alternative port
- Or kill the process: `lsof -ti:3000 | xargs kill -9`

**API connection error:**
- Make sure the backend is running on port 8000
- Check that `VITE_API_URL` in `.env` is correct
- Try accessing http://localhost:8000/health in your browser

### Both Running But Can't Login

**CORS Error:**
- Check that `ALLOWED_ORIGINS` in backend `.env` includes `http://localhost:3000`
- Restart the backend server after changing `.env`

## Next Steps

- 📖 Read the [API Documentation](http://localhost:8000/docs)
- 🚀 Learn about [Deployment](../README.md#deployment)
- 🔧 Customize the agent in `backend/agent.py`
- 🎨 Modify the UI in `frontend/src/`
- 🛠️ Explore the [MCP Integration Guide](MCP_INTEGRATION.md)
- 📝 View [Recent Updates](UPDATES.md) for latest features

## Key Features to Try

### Enhanced Logging & Debugging
- **Backend Console**: Shows detailed logs for every request
  - User information and message preview
  - Current model and requested model
  - Model switching operations (old → new)
  - MCP tool calls and responses
- **Frontend Console**: Open browser DevTools (F12) to see:
  - Model selection: `🔄 Model selected in UI: <model-id>`
  - Request details: `📤 Sending message with model: <model-id>`
- Perfect for debugging model switching and API issues

### Chat Interface
- Long messages automatically wrap without expanding window width
- Proper handling of URLs and long text
- Code blocks scroll horizontally when needed
- **Markdown Rendering**: Full GitHub Flavored Markdown support
- **Rich Formatting**: Lists, tables, code blocks, and more
- Smooth animations and responsive design

### Model Selection
- Click "🤖 Models" to view available LLM models
- Choose between different Groq-hosted models
- See model descriptions, context windows, and providers
- Current model displays in the selector

### Tool Discovery
- Click "Show Tools" to see all available tools
- View tool descriptions and parameters
- Tools from MCP servers are highlighted

## Development Tips

### Backend Hot Reload

For automatic reload on code changes:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Hot Reload

The dev server automatically reloads when you edit files.

### Viewing Logs

Backend logs appear in the terminal where you ran `python main.py`.

### Testing API Endpoints

Use the Swagger UI at http://localhost:8000/docs to test API endpoints directly.

## Getting Help

If you encounter issues:

1. Check the terminal output for error messages
2. Verify all prerequisites are installed
3. Ensure all environment variables are set correctly
4. Make sure both servers are running simultaneously
5. Check the troubleshooting section above

For additional help, please open an issue on GitHub.

---

Happy coding! 🚀
