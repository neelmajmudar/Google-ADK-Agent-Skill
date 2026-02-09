# Evaluation Scenarios

## Eval 1: Basic Single Agent with Tools

**Prompt**: "Create an ADK agent that can look up stock prices and convert currencies."

**Expected behavior**:
- Creates proper project structure (agent.py, __init__.py, .env)
- Defines two function tools with complete docstrings, type hints, Args/Returns
- Tools return dicts with status fields
- Agent has clear instruction referencing both tools by name
- Uses `root_agent` variable name
- Model string is valid (e.g., "gemini-2.5-flash")

## Eval 2: Multi-Agent Pipeline

**Prompt**: "Build an ADK agent system where one agent extracts data from text, another validates it, and a third formats it as JSON."

**Expected behavior**:
- Uses SequentialAgent with three LlmAgent sub-agents
- Each agent has output_key for state sharing
- Later agents reference earlier outputs via {state_key} in instructions
- Pipeline order is logical (extract → validate → format)

## Eval 3: Stateful Agent with ToolContext

**Prompt**: "Create an ADK agent for a quiz app that tracks the user's score across questions using session state."

**Expected behavior**:
- Tool functions include `tool_context: ToolContext` parameter
- State reads/writes use tool_context.state
- Uses appropriate key prefix (user: for cross-session persistence)
- Instruction references state variables with {key} syntax
- Does not document tool_context in the docstring
