# Changelog

All notable changes to MooAgent will be documented in this file.

## [2.4.0] - 2026-01-24

### Added
- Enhanced logging system for model switching and chat requests
  - Frontend console logs for model selection (`🔄 Model selected in UI`)
  - Frontend request logs showing which model is being sent (`📤 Sending message with model`)
  - Backend logs showing user info, message preview, and model status
  - Model switch confirmation with old → new model display
- Warning suppression for harmless LangSmith API key warnings
- Detailed debugging capabilities in both frontend and backend

### Changed
- Default model set to `llama-3.3-70b-versatile` for best MCP compatibility
- Model order in UI: LLaMA models first (recommended), OpenAI models second
- Simplified agent architecture - removed complex wrapper classes
- Improved developer experience with cleaner console output

### Fixed
- LangSmith warning messages no longer appear in console
- Model switching now properly logged and trackable
- All LangChain dependency conflicts resolved

## [2.3.0] - 2026-01-23

### Added
- Model selector UI component with 4 available models
- Dynamic model switching via API
- Full markdown rendering with GitHub Flavored Markdown (GFM)
- Support for lists, tables, code blocks, and inline formatting
- Clickable links in agent responses
- Text wrapping improvements to prevent horizontal overflow

### Changed
- Updated LangChain packages to latest compatible versions:
  - `langchain==0.2.16`
  - `langchain-groq==0.1.9`
  - `langchain-community==0.2.16`
  - `langgraph==0.2.28`
- Improved markdown list rendering (removed extra line breaks)
- Better CSS for inline elements within lists

### Fixed
- Dependency conflicts between LangChain packages
- Extra line breaks in markdown lists
- Paragraphs rendering incorrectly inside list items
- Model decommissioning errors with automatic fallback

## [2.2.0] - 2026-01-22

### Added
- Test MCP server with 4 example tools (calculator, weather, time, uuid)
- Tool discovery UI with "Show Tools" button
- `/agent/tools` API endpoint
- Thread-based async execution for MCP calls
- Adobe HelpX tool integration for documentation queries

### Changed
- Increased agent max iterations from 3 to 10
- Added 30-second timeout for agent execution
- Improved MCP tool descriptions and error handling

### Fixed
- uvloop compatibility issues with async operations
- "Transport closed" errors in MCP calls
- Async coroutine not awaited warnings
- Agent iteration limit errors

## [2.1.0] - 2026-01-21

### Added
- MCP (Model Context Protocol) integration
- Remote tool access via MCP servers
- Dynamic tool discovery from MCP endpoints
- `mcp_agent.py` for MCP sub-agent functionality

### Changed
- Updated agent to support extensible tool framework
- Added MCP_SERVER_URL configuration option

## [2.0.0] - 2026-01-20

### Added
- Complete backend with FastAPI
- React TypeScript frontend
- JWT authentication system
- Groq LLaMA integration
- LangChain agent orchestration
- Dark theme UI
- Responsive design
- User registration and login
- Chat interface
- Deployment configurations for Fly.io and Vercel

### Changed
- Migrated from initialize_agent to create_react_agent (LangChain update)

### Fixed
- Password length validation (72-byte bcrypt limit)
- Registration failures
- Authentication token handling

## [1.0.0] - 2026-01-15

### Added
- Initial project structure
- Basic documentation
- Product Requirements Document (PRD)
- Architecture diagrams

---

## Version Numbering

- **Major** (X.0.0): Breaking changes, major new features
- **Minor** (0.X.0): New features, enhancements, non-breaking changes
- **Patch** (0.0.X): Bug fixes, minor improvements

## Links

- [Full Updates Document](UPDATES.md)
- [Product Requirements](prd.md)
- [Getting Started Guide](GETTING_STARTED.md)
- [API Documentation](API.md)
