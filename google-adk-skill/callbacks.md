# Callbacks

Callbacks hook into an agent's execution at key points. Return `None` to proceed normally, or return content to override.

## Callback Types

| Callback | Trigger Point | Return to Override |
|----------|--------------|-------------------|
| `before_agent_callback` | Before agent starts processing | `types.Content` to skip agent |
| `after_agent_callback` | After agent finishes | `types.Content` to replace output |
| `before_model_callback` | Before LLM call | `LlmResponse` to skip LLM |
| `after_model_callback` | After LLM responds | `LlmResponse` to replace response |
| `before_tool_callback` | Before tool executes | `dict` to skip tool execution |
| `after_tool_callback` | After tool executes | `dict` to replace tool result |

## Registration

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from typing import Optional

def my_guardrail(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """Block requests containing forbidden topics."""
    last_msg = llm_request.contents[-1].parts[0].text if llm_request.contents else ""
    if "forbidden_topic" in last_msg.lower():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I cannot help with that topic.")]
            )
        )
    return None  # Proceed to LLM

agent = LlmAgent(
    name="GuardedAgent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant.",
    before_model_callback=my_guardrail,
)
```

## Common Patterns

### Input Guardrail (before_model_callback)

Check `llm_request.contents` for policy violations. Return `LlmResponse` to block.

### Output Modifier (after_agent_callback)

```python
def add_disclaimer(callback_context: CallbackContext) -> Optional[types.Content]:
    if callback_context.state.get("add_disclaimer"):
        return types.Content(role="model", parts=[types.Part(text="[Disclaimer added] ...")])
    return None
```

### State Mutation (before_agent_callback)

```python
def track_visits(callback_context: CallbackContext) -> Optional[types.Content]:
    count = callback_context.state.get("visits", 0)
    callback_context.state["visits"] = count + 1
    return None  # Always proceed
```

### Tool Auth Check (before_tool_callback)

```python
from google.adk.tools import ToolContext

def check_auth(tool_context: ToolContext, tool_name: str, args: dict) -> Optional[dict]:
    if not tool_context.state.get("auth_token"):
        tool_context.request_credential(auth_config)
        return {"error": "Authentication required"}
    return None  # Proceed with tool
```

### Skip Summarization (after_tool_callback)

```python
def raw_output(tool_context: ToolContext, tool_name: str, result: dict) -> Optional[dict]:
    tool_context.actions.skip_summarization = True
    return None  # Use original result but skip LLM summarization
```

### Logging

```python
def log_model_call(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    print(f"[{callback_context.agent_name}] Model call with {len(llm_request.contents)} messages")
    return None
```
