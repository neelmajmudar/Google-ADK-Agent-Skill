# Running and Deploying ADK Agents

## Development: InMemoryRunner

Simplest way to run an agent. No persistence — all data lost on restart.

```python
import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types

# Assuming agent is defined in agent.py
from my_agent.agent import root_agent

runner = InMemoryRunner(agent=root_agent, app_name="my_app")

async def main():
    # Quick debug run (ADK ≥ 1.18)
    response = await runner.run_debug("Hello, what can you do?")

asyncio.run(main())
```

### Programmatic run with session control

```python
async def chat():
    session_service = runner.session_service
    user_id = "user_1"
    session_id = "session_1"

    await session_service.create_session(
        app_name="my_app", user_id=user_id, session_id=session_id
    )

    message = types.Content(role="user", parts=[types.Part(text="What's the weather in NYC?")])

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message
    ):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)
```

## Development: CLI Commands

```bash
# Browser-based dev UI (recommended for debugging)
adk web my_agent/

# Terminal interaction
adk run my_agent/

# REST API server
adk api_server my_agent/
```

All commands expect the parent directory of your agent folder. The agent folder must contain `agent.py` with `root_agent` defined.

## Production: Runner with Persistent Services

```python
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService  # or VertexAiMemoryBankService

session_service = DatabaseSessionService(db_url="sqlite:///sessions.db")
memory_service = InMemoryMemoryService()

runner = Runner(
    agent=root_agent,
    app_name="my_app",
    session_service=session_service,
    memory_service=memory_service,
)
```

## Deployment: Cloud Run

```bash
# One-command deploy (requires gcloud CLI configured)
adk deploy cloud_run \
    --project=YOUR_PROJECT_ID \
    --region=us-central1 \
    my_agent/
```

## Deployment: Vertex AI Agent Engine

```python
import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(project="YOUR_PROJECT", location="us-central1")

app = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)

remote_app = reasoning_engines.ReasoningEngine.create(
    app,
    requirements=["google-adk", "google-cloud-aiplatform"],
)

# Test deployed agent
response = remote_app.query(input="Hello!", user_id="user_1", session_id="s1")
```

## App Class (Optional, for Complex Projects)

The `App` class centralizes configuration for complex agent workflows:

```python
from google.adk.apps import App

app = App(
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service,
)
```

Run with `InMemoryRunner(app=app)` or via CLI.
