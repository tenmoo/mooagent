# Troubleshooting: Agent Format Errors

## Issue: "Agent stopped due to iteration limit or time limit"

### Symptoms
- Agent responds with: `Could not parse LLM output`
- Error message: `Your output format was incorrect`
- Agent only writes `Thought:` but not `Action:` and `Action Input:`

### Root Cause
The LLM is not completing the full ReAct format. It stops after writing the `Thought:` line and doesn't continue with the required `Action:` and `Action Input:` lines.

### Solution 1: Use LLaMA Models (Recommended)

**Problem:** OpenAI GPT-OSS models have known compatibility issues with LangChain's ReAct format.

**Fix:** Switch to LLaMA models which are more reliable:

1. **In the UI:** Select "LLaMA 3.3 70B" or "LLaMA 3.1 8B Instant" from the model selector
2. **In config:** The default has been changed to `llama-3.3-70b-versatile`

```python
# backend/config.py
default_model: str = "llama-3.3-70b-versatile"  # ✅ Reliable
# NOT: "openai/gpt-oss-120b"  # ❌ Has format issues
```

### Solution 2: Enhanced Prompt (Already Applied)

The prompt has been updated with:

1. **Explicit warnings** about completing the format
2. **Visual emphasis** with ⚠️ symbols
3. **Clear examples** showing ALL required lines
4. **Stronger error messages** that explain exactly what went wrong

### Solution 3: Increase Iterations/Time

If using LLaMA and still getting timeouts:

```python
# backend/agent.py - AgentExecutor configuration
max_iterations=15,  # Increase from 10
max_execution_time=45,  # Increase from 30
```

### Solution 4: Simplify Tool Detection

If the agent is struggling to decide which tool to use:

```python
# backend/mcp_agent.py - call_mcp_tool
# The logic already defaults to HelpX for most queries
# Ensure MCP server is responding quickly
```

---

## Testing the Fix

### 1. Restart the Backend
```bash
cd /Users/chien/Github/tenmoo/mooagent/backend
python main.py
```

### 2. Test with Simple Query
In the UI, ask:
```
How to crop in Photoshop?
```

### 3. Expected Behavior
You should see in the console:
```
🤖 Agent Processing Query: How to crop in Photoshop?
🎯 Detected tool: helpx
📤 MCP Result: Found X Adobe HelpX articles...
✅ Response generated successfully
```

### 4. Check the Response Format
The agent should output:
```
Thought: This is about Photoshop cropping, I need Adobe docs.
Action: MCPRemoteTool
Action Input: how to crop in Photoshop
```

NOT just:
```
Thought: This is about Photoshop cropping, I need Adobe docs.
[STOPS HERE - ERROR!]
```

---

## Model Comparison

### ✅ Recommended: LLaMA Models
**LLaMA 3.3 70B** (`llama-3.3-70b-versatile`)
- ✅ Excellent ReAct format compliance
- ✅ Reliable tool calling
- ✅ Good reasoning abilities
- Speed: 280 tokens/sec

**LLaMA 3.1 8B** (`llama-3.1-8b-instant`)
- ✅ Very fast responses
- ✅ Good format compliance
- ⚠️ Slightly less sophisticated reasoning
- Speed: 560 tokens/sec

### ⚠️ Problematic: OpenAI Models
**GPT-OSS 120B** (`openai/gpt-oss-120b`)
- ❌ Inconsistent ReAct format compliance
- ❌ Often stops after "Thought:"
- ❌ May require multiple retries
- ✅ Strong reasoning when it works
- Speed: 500 tokens/sec

**GPT-OSS 20B** (`openai/gpt-oss-20b`)
- ❌ Similar format issues
- Speed: 1000 tokens/sec

---

## Additional Debugging

### Enable Verbose Logging
```python
# backend/config.py
debug: bool = True
```

This will show:
- Full agent scratchpad
- Tool selection process
- Parsing errors
- MCP server communication

### Check Console Output
Look for these indicators:

**✅ Good:**
```
📊 Agent Response Keys: dict_keys(['output', 'intermediate_steps'])
🔧 Tool Usage Steps: 1
  Step 1:
    Tool: MCPRemoteTool
    Input: how to crop in Photoshop
    Output: Found 5 Adobe HelpX articles...
```

**❌ Bad:**
```
Could not parse LLM output: `Thought: ...`
Your output format was incorrect.
Agent stopped due to iteration limit
```

### Test MCP Server Directly
```bash
# Test if MCP server is responding
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```

Should return:
```json
{
  "jsonrpc": "2.0",
  "result": {"tools": [...]},
  "id": 1
}
```

---

## Quick Fix Checklist

- [ ] Switch to LLaMA model (not OpenAI)
- [ ] Restart backend server
- [ ] Test with simple query: "How to crop in Photoshop?"
- [ ] Check console logs for tool usage
- [ ] Verify MCP server is running and responding
- [ ] If still failing, enable debug mode
- [ ] If still failing, increase max_iterations to 15

---

## When to Use Each Model

### Use LLaMA 3.3 70B when:
- You need reliable tool calling
- Format compliance is critical
- Complex Adobe workflows
- Default choice ✅

### Use LLaMA 3.1 8B when:
- Speed is critical
- Simple queries
- Testing/development

### Avoid OpenAI models when:
- Tool calling is required
- ReAct format is critical
- Reliability is more important than reasoning

### Can try OpenAI models when:
- Not using tools (direct Q&A)
- Can tolerate retries
- Need very strong reasoning for complex explanations

---

*Last updated: January 26, 2026*
*Related docs: `docs/PROMPT_ENGINEERING_CHANGES.md`, `docs/PROMPT_ENGINEERING_QUICK_REF.md`*
