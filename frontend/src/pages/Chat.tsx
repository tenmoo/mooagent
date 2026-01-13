import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { useChatStore } from '../store/chatStore';
import { apiService } from '../services/api';
import '../styles/Chat.css';

export default function Chat() {
  const { user, logout } = useAuthStore();
  const { messages, isLoading, sendMessage, clearMessages } = useChatStore();
  const [input, setInput] = useState('');
  const [showTools, setShowTools] = useState(false);
  const [tools, setTools] = useState<any>(null);
  const [loadingTools, setLoadingTools] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleLoadTools = async () => {
    if (tools) {
      setShowTools(!showTools);
      return;
    }
    
    setLoadingTools(true);
    try {
      const toolsData = await apiService.getAgentTools();
      setTools(toolsData);
      setShowTools(true);
    } catch (error) {
      console.error('Failed to load tools:', error);
    } finally {
      setLoadingTools(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const message = input.trim();
    setInput('');

    try {
      await sendMessage(message);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const formatTime = (date: Date) => {
    return new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-content">
          <h1>🐄 Moo</h1>
          <div className="header-actions">
            <span className="user-info">{user?.email}</span>
            <button onClick={handleLoadTools} className="btn-secondary">
              {loadingTools ? 'Loading...' : showTools ? 'Hide Tools' : 'Show Tools'}
            </button>
            <button onClick={clearMessages} className="btn-secondary">
              Clear Chat
            </button>
            <button onClick={logout} className="btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="chat-messages">
        {showTools && tools && (
          <div className="tools-panel">
            <h3>🛠️ Available Tools</h3>
            
            <div className="tools-section">
              <h4>Built-in Tools</h4>
              {tools.built_in_tools?.map((tool: any, index: number) => (
                <div key={index} className="tool-item">
                  <strong>{tool.name}</strong>
                  <p>{tool.description}</p>
                </div>
              ))}
            </div>

            {tools.mcp_server_url && (
              <div className="tools-section">
                <h4>MCP Tools ({tools.mcp_server_url})</h4>
                {tools.mcp_tools && tools.mcp_tools.length > 0 ? (
                  tools.mcp_tools.map((tool: any, index: number) => (
                    <div key={index} className="tool-item mcp-tool">
                      <strong>{tool.name}</strong>
                      <p>{tool.description}</p>
                      {tool.parameters && (
                        <details>
                          <summary>Parameters</summary>
                          <pre>{JSON.stringify(tool.parameters, null, 2)}</pre>
                        </details>
                      )}
                    </div>
                  ))
                ) : (
                  <p className="no-tools">
                    {tools.mcp_error 
                      ? `Error: ${tools.mcp_error}` 
                      : 'No MCP tools available'}
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {messages.length === 0 ? (
          <div className="empty-state">
            <h2>Welcome to Moo!</h2>
            <p>Your AI-powered personal assistant is ready to help.</p>
            <div className="suggestions">
              <button
                onClick={() => setInput('Help me plan my day')}
                className="suggestion"
              >
                Help me plan my day
              </button>
              <button
                onClick={() => setInput('What can you help me with?')}
                className="suggestion"
              >
                What can you help me with?
              </button>
              <button
                onClick={() => setInput('Tell me about yourself')}
                className="suggestion"
              >
                Tell me about yourself
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-avatar">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-role">
                      {message.role === 'user' ? 'You' : 'MooAgent'}
                    </span>
                    <span className="message-time">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-container">
        <div className="chat-input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="btn-send"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M22 2L11 13"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M22 2L15 22L11 13L2 9L22 2Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
}
