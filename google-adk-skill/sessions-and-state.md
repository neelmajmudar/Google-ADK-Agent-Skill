# Sessions, State, and Memory

## Sessions

A Session tracks one conversation thread: its history (Events), state, and identifiers.

```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
session = await session_service.create_session(
    app_name="my_app",
    user_id="user_123",
    state={"initial_key": "value"},  # Optional initial state
)
```

### Session Services

| Service | Persistence | Use For |
|---------|-------------|---------|
| `InMemorySessionService` | None (lost on restart) | Local dev, testing |
| `DatabaseSessionService` | SQLite/PostgreSQL | Self-hosted production |
| `VertexAiSessionService` | Google Cloud | Managed production |

## State

State is a dict-like store on the session. Modifications are tracked as deltas in Events.

### State Key Prefixes

| Prefix | Scope | Persists Across Sessions? |
|--------|-------|--------------------------|
| (none) | Current session only | No |
| `user:` | All sessions for this user | Yes |
| `app:` | All sessions for all users | Yes |
| `temp:` | Current invocation only | No (not even across turns) |

```python
# In a tool or callback:
context.state["session_only_key"] = "gone after session ends"
context.state["user:preference"] = "dark_mode"   # persists per user
context.state["app:api_endpoint"] = "https://..."  # global
context.state["temp:scratch"] = "discarded after this turn"
```

### Reading State in Instructions

Use `{key}` in agent instructions to auto-inject state values:

```python
agent = LlmAgent(
    instruction="The user prefers {user:preference}. Respond accordingly.",
)
```

### Writing State from Tools

```python
from google.adk.tools import ToolContext

def update_prefs(new_pref: str, tool_context: ToolContext) -> dict:
    """Updates the user's display preference."""
    tool_context.state["user:preference"] = new_pref
    return {"status": "updated"}
```

### Writing State from Callbacks

```python
from google.adk.agents.callback_context import CallbackContext

def my_before_agent(callback_context: CallbackContext):
    count = callback_context.state.get("visit_count", 0)
    callback_context.state["visit_count"] = count + 1
    return None  # proceed normally
```

## Memory (Cross-Session Recall)

Memory enables agents to recall information from past sessions.

### InMemoryMemoryService (dev/testing)

```python
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory

memory_service = InMemoryMemoryService()

agent = LlmAgent(
    instruction="Answer questions. Use 'load_memory' if the answer might be in past conversations.",
    tools=[load_memory],
)

runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service,
    memory_service=memory_service,
)
```

### VertexAiMemoryBankService (production)

```python
from google.adk.memory import VertexAiMemoryBankService

memory_service = VertexAiMemoryBankService(
    project="my-project",
    location="us-central1",
    agent_engine_id="your_engine_id",
)
```

Memory Bank uses Gemini to extract key information from session data for efficient long-term storage.

### Memory Tools

| Tool | Behavior |
|------|----------|
| `load_memory` | Agent calls it on-demand to search past conversations |
| `PreloadMemory` | Automatically retrieves relevant memories at start of each turn |
