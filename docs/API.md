# API Documentation

Complete API reference for MooAgent backend.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-app.fly.dev`

## Authentication

Most endpoints require authentication using Bearer tokens (JWT).

Include the token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Health & Info

#### GET /

Get API information.

**Response:**
```json
{
  "message": "Welcome to MooAgent API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Authentication

#### POST /auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"  // optional
}
```

**Response:** `201 Created`
```json
{
  "id": "user@example.com",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2026-01-11T12:00:00",
  "is_active": true
}
```

**Errors:**
- `400`: Email already registered
- `422`: Validation error (invalid email, password too short)

---

#### POST /auth/login

Login with email and password to receive a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401`: Incorrect email or password

**Usage:**
Store the `access_token` and include it in subsequent requests:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

#### GET /auth/me

Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": "user@example.com",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2026-01-11T12:00:00",
  "is_active": true
}
```

**Errors:**
- `401`: Invalid or expired token

---

### Chat

#### POST /chat

Send a message to the AI agent and receive a response.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "message": "Help me plan my day",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello!"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you today?"
    }
  ]
}
```

**Fields:**
- `message` (string, required): The user's message
- `conversation_history` (array, optional): Previous messages for context

**Message Object:**
- `role` (string): One of "user", "assistant", or "system"
- `content` (string): The message content

**Response:** `200 OK`
```json
{
  "response": "I'd be happy to help you plan your day! To create an effective daily plan, I'll need to know...",
  "conversation_id": null
}
```

**Errors:**
- `401`: Invalid or expired token
- `500`: Error processing the chat message

**Example Usage:**

```javascript
// First message (no history)
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "What can you help me with?"
  })
});

// Follow-up message (with history)
const response2 = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "Tell me more about the first one",
    conversation_history: [
      {
        role: "user",
        content: "What can you help me with?"
      },
      {
        role: "assistant",
        content: "I can help you with various tasks..."
      }
    ]
  })
});
```

---

#### GET /agent/info

Get information about the AI agent.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "name": "MooAgent",
  "description": "AI-powered personal assistant",
  "system_prompt": "You are MooAgent, an AI-powered personal assistant...",
  "model": "OpenAI GPT-OSS 120B or Meta LLaMA (Groq-hosted)",
  "current_model": "openai/gpt-oss-120b"
}
```

**Errors:**
- `401`: Invalid or expired token

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Example Error Response

```json
{
  "detail": "Could not validate credentials"
}
```

---

## Rate Limiting

Currently, there are no rate limits enforced. In production, consider implementing rate limiting to prevent abuse.

---

## CORS

The API supports CORS for origins specified in the `ALLOWED_ORIGINS` environment variable.

**Default (development):**
- `http://localhost:3000`

**Production:**
Configure via environment variable to match your frontend domain.

---

## Testing the API

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Chat:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"Hello!"}'
```

### Using Swagger UI

Visit `http://localhost:8000/docs` for an interactive API documentation where you can test all endpoints.

1. Click on an endpoint
2. Click "Try it out"
3. Fill in the parameters
4. Click "Execute"

### Using Python

```python
import requests

# Register
response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "email": "test@example.com",
        "password": "password123"
    }
)
print(response.json())

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    json={
        "email": "test@example.com",
        "password": "password123"
    }
)
token = response.json()["access_token"]

# Chat
response = requests.post(
    "http://localhost:8000/chat",
    headers={"Authorization": f"Bearer {token}"},
    json={"message": "Hello!"}
)
print(response.json())
```

---

## Webhooks

Not currently supported. May be added in future versions.

---

## Versioning

Current version: `1.0.0`

The API version may be included in the URL path in future releases (e.g., `/v1/chat`).

---

## Support

For issues or questions about the API:
- Open an issue on GitHub
- Check the interactive documentation at `/docs`
- Review the source code in `backend/main.py`
