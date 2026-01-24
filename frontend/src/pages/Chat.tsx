import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { useChatStore } from '../store/chatStore';
import { apiService } from '../services/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../styles/Chat.css';

export default function Chat() {
  const { user, logout } = useAuthStore();
  const { messages, isLoading, sendMessage, clearMessages, selectedModel, setSelectedModel, error, clearError } = useChatStore();
  const [input, setInput] = useState('');
  const [showTools, setShowTools] = useState(false);
  const [showModels, setShowModels] = useState(false);
  const [tools, setTools] = useState<any>(null);
  const [models, setModels] = useState<any>(null);
  const [loadingTools, setLoadingTools] = useState(false);
  const [loadingModels, setLoadingModels] = useState(false);
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

  const handleLoadModels = async () => {
    if (models) {
      setShowModels(!showModels);
      return;
    }
    
    setLoadingModels(true);
    try {
      const modelsData = await apiService.getAvailableModels();
      setModels(modelsData);
      setShowModels(true);
      // Set initial model if not already set
      if (!selectedModel && modelsData.current_model) {
        setSelectedModel(modelsData.current_model);
      }
    } catch (error) {
      console.error('Failed to load models:', error);
    } finally {
      setLoadingModels(false);
    }
  };

  const handleModelSelect = (modelId: string) => {
    console.log('🔄 Model selected in UI:', modelId);
    setSelectedModel(modelId);
    setShowModels(false);
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

  const renderMessageWithLinks = (text: string) => {
    // Regular expression to detect URLs
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);

    return parts.map((part, index) => {
      // Check if this part is a URL
      if (part.match(urlRegex)) {
        return (
          <a
            key={index}
            href={part}
            target="_blank"
            rel="noopener noreferrer"
            className="message-link"
          >
            {part}
          </a>
        );
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-content">
          <div className="header-actions">
            <span className="user-info">{user?.email}</span>
            <button onClick={handleLoadModels} className="btn-secondary">
              {loadingModels ? 'Loading...' : showModels ? 'Hide Models' : '🤖 Models'}
            </button>
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
        {showModels && models && (
          <div className="models-panel">
            <h3>🤖 Select LLM Model</h3>
            <p className="panel-subtitle">Current: {models.models.find((m: any) => m.id === selectedModel)?.name || selectedModel}</p>
            
            <div className="models-grid">
              {models.models?.map((model: any) => (
                <div 
                  key={model.id} 
                  className={`model-card ${selectedModel === model.id ? 'selected' : ''}`}
                  onClick={() => handleModelSelect(model.id)}
                >
                  <div className="model-header">
                    <strong>{model.name}</strong>
                    {selectedModel === model.id && <span className="badge">Active</span>}
                  </div>
                  <p className="model-description">{model.description}</p>
                  <div className="model-footer">
                    <span className="model-provider">{model.provider === 'openai' ? '🔵 OpenAI' : '⚡ Groq'}</span>
                    <span className="model-context">{model.context_window.toLocaleString()} tokens</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

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

        {error && (
          <div className="error-banner">
            <div className="error-content">
              <span className="error-icon">⚠️</span>
              <span className="error-message">{error}</span>
              <button className="error-close" onClick={clearError}>✕</button>
            </div>
          </div>
        )}

        {messages.length === 0 ? (
          <div className="empty-state">
            <h2>Welcome to MooAgent!</h2>
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
                  <div className="message-text">
                    {message.role === 'assistant' ? (
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          a: ({ node, ...props }) => (
                            <a {...props} target="_blank" rel="noopener noreferrer" className="message-link" />
                          ),
                          code: ({ node, inline, ...props }: any) => (
                            inline ? (
                              <code className="inline-code" {...props} />
                            ) : (
                              <code className="code-block" {...props} />
                            )
                          ),
                          // Remove paragraph wrappers entirely from list items
                          li: ({ node, children, ...props }: any) => {
                            return <li {...props} className="markdown-li">{children}</li>;
                          },
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    ) : (
                      renderMessageWithLinks(message.content)
                    )}
                  </div>
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
