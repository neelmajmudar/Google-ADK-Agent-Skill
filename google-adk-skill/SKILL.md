---
name: building-google-adk-agents
description: Build AI agents using Google's Agent Development Kit (ADK). Use when creating ADK agents, defining tools, configuring multi-agent systems, setting up sessions/state/memory, writing callbacks, running agents with Runner, or deploying to Cloud Run or Vertex AI Agent Engine. Covers LlmAgent, workflow agents (Sequential, Parallel, Loop), custom agents, function tools, MCP tools, ToolContext, and the ADK project structure.
---

# Building Google ADK Agents

## Quick Start

ADK agents require a `root_agent` definition in `agent.py`. Minimal agent:

```python
from google.adk.agents import Agent

def my_tool(query: str) -> dict:
    """Does something useful. Args: query: The search query. Returns: dict with status and result."""
    return {"status": "success", "result": f"Processed: {query}"}

root_agent = Agent(
    model="gemini-2.5-flash",
    name="my_agent",
    description="Handles user requests.",
    instruction="You are a helpful assistant. Use 'my_tool' when the user asks you to process something.",
    tools=[my_tool],
)
```

Install: `pip install google-adk`

Run: `adk web` (browser UI) or `adk run <agent_folder>` (terminal)

## Project Structure

```
my_agent/
├── __init__.py        # Empty or imports
├── agent.py           # Must define root_agent (or app for App-based agents)
├── .env               # API keys (GOOGLE_API_KEY or GOOGLE_GENAI_USE_VERTEXAI + project)
└── tools/             # Optional: separate tool modules
```

The `.env` file should contain one of:

```bash
# Option A: Google AI Studio (free tier)
GOOGLE_API_KEY=your_key_here

# Option B: Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Core Concepts

### Agent Types

| Type | Use When | LLM-Powered? |
|------|----------|--------------|
| `LlmAgent` / `Agent` | Dynamic reasoning, tool use, conversation | Yes |
| `SequentialAgent` | Fixed pipeline (A → B → C) | No (orchestration only) |
| `ParallelAgent` | Independent tasks run concurrently | No |
| `LoopAgent` | Repeat until condition met | No |
| `BaseAgent` (custom) | Unique control flow not covered above | Your choice |

### LlmAgent Key Parameters

```python
Agent(
    name="agent_name",              # Required, unique identifier
    model="gemini-2.5-flash",       # Required, LLM model string
    description="What this does",   # Recommended for multi-agent routing
    instruction="Your persona...",  # Core behavior guidance
    tools=[tool1, tool2],           # Functions, BaseTool, or AgentTool
    output_key="result_key",        # Auto-save response to state[key]
    output_schema=MyPydanticModel,  # Enforce structured JSON output
    sub_agents=[agent_a, agent_b],  # For LLM-driven delegation
    include_contents="default",     # "default" or "none" (stateless)
)
```

**State templating in instructions**: Use `{variable_name}` to inject `session.state["variable_name"]` into the instruction at runtime. Use `{var?}` to silently ignore missing keys.

### Tools — Defining Effective Function Tools

The LLM reads the function name, docstring, type hints, and parameter descriptions to decide when/how to call it.

```python
def get_weather(city: str) -> dict:
    """Retrieves the current weather for a city.

    Args:
        city: The city name (e.g., "New York", "London").

    Returns:
        dict with 'status' and 'report' or 'error_message'.
    """
    # Implementation here
    return {"status": "success", "report": "Sunny, 25°C"}
```

**Guidelines**:
- Use descriptive verb-noun names: `get_weather`, `search_documents`, `send_email`
- Always include type hints and a complete docstring with Args/Returns
- Return dicts (not raw strings) for structured data
- Do NOT document `tool_context` in the docstring — it's injected by ADK automatically

### ToolContext — Accessing Session State in Tools

```python
from google.adk.tools import ToolContext

def my_stateful_tool(query: str, tool_context: ToolContext) -> dict:
    """Processes query using session context."""
    # Read state
    user_pref = tool_context.state.get("user_preference", "default")
    # Write state (automatically tracked in event delta)
    tool_context.state["last_query"] = query
    return {"result": f"Processed with pref={user_pref}"}
```

### Multi-Agent Patterns

See [reference/multi-agent-patterns.md](reference/multi-agent-patterns.md) for:
- Sequential pipelines with `output_key` and state sharing
- Parallel fan-out / fan-in with `ParallelAgent`
- LLM-driven delegation via `sub_agents`
- Agent-as-Tool pattern via `AgentTool`
- Custom orchestrators extending `BaseAgent`

### Sessions, State, and Memory

See [reference/sessions-and-state.md](reference/sessions-and-state.md) for:
- `InMemorySessionService` vs persistent services
- State key prefixes: `user:` (cross-session per user), `app:` (global), `temp:` (not persisted)
- Memory services for cross-session recall (`InMemoryMemoryService`, `VertexAiMemoryBankService`)

### Callbacks

See [reference/callbacks.md](reference/callbacks.md) for:
- `before_agent_callback` / `after_agent_callback`
- `before_model_callback` / `after_model_callback`
- `before_tool_callback` / `after_tool_callback`
- Guardrail, caching, logging, and state mutation patterns

### Running Agents

See [reference/running-and-deploying.md](reference/running-and-deploying.md) for:
- `InMemoryRunner` for development
- `Runner` with persistent session/memory services for production
- `adk web`, `adk run`, `adk api_server` CLI commands
- Cloud Run and Vertex AI Agent Engine deployment

## Workflow: Building an ADK Agent

```
Task Progress:
- [ ] Step 1: Define requirements (what the agent does, tools needed)
- [ ] Step 2: Create project structure (agent folder, .env, __init__.py)
- [ ] Step 3: Implement tools (function tools with proper docstrings)
- [ ] Step 4: Define agent(s) (LlmAgent with instruction, tools, sub_agents)
- [ ] Step 5: Wire up Runner (InMemoryRunner for dev, Runner for prod)
- [ ] Step 6: Test with `adk web` or programmatic runner
- [ ] Step 7: Iterate on instructions and tool descriptions
```
