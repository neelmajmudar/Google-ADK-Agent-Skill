# Multi-Agent Patterns

## 1. Sequential Pipeline

Agents run in order. Use `output_key` to pass results via `session.state`.

```python
from google.adk.agents import SequentialAgent, LlmAgent

writer = LlmAgent(
    name="Writer",
    model="gemini-2.5-flash",
    instruction="Write Python code based on the user's request. Output only the code block.",
    output_key="generated_code",
)

reviewer = LlmAgent(
    name="Reviewer",
    model="gemini-2.5-flash",
    instruction="Review the code in {generated_code}. List issues as bullet points.",
    output_key="review_comments",
)

refactorer = LlmAgent(
    name="Refactorer",
    model="gemini-2.5-flash",
    instruction="Refactor the code from {generated_code} using feedback from {review_comments}.",
    output_key="final_code",
)

root_agent = SequentialAgent(
    name="CodePipeline",
    sub_agents=[writer, reviewer, refactorer],
)
```

## 2. Parallel Fan-Out / Fan-In

Independent tasks run concurrently, then a synthesizer combines results.

```python
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent

fetch_news = LlmAgent(name="NewsFetcher", instruction="Find recent news about {topic}.", output_key="news_data")
fetch_stats = LlmAgent(name="StatsFetcher", instruction="Find statistics about {topic}.", output_key="stats_data")

gather = ParallelAgent(name="ParallelGather", sub_agents=[fetch_news, fetch_stats])

synthesizer = LlmAgent(
    name="Synthesizer",
    instruction="Combine the news from {news_data} and stats from {stats_data} into a report.",
)

root_agent = SequentialAgent(name="ResearchPipeline", sub_agents=[gather, synthesizer])
```

## 3. LLM-Driven Delegation (sub_agents)

The coordinator LLM decides which sub-agent to hand off to based on descriptions.

```python
billing_agent = LlmAgent(
    name="BillingAgent",
    model="gemini-2.5-flash",
    description="Handles billing inquiries, invoices, and payment issues.",
    instruction="You handle billing questions. Be precise about amounts and dates.",
)

support_agent = LlmAgent(
    name="SupportAgent",
    model="gemini-2.5-flash",
    description="Handles technical support, bug reports, and troubleshooting.",
    instruction="You handle technical support. Ask for error messages and steps to reproduce.",
)

root_agent = LlmAgent(
    name="Router",
    model="gemini-2.5-flash",
    description="Routes user requests to the appropriate specialist.",
    instruction="Analyze the user's request and transfer to the appropriate specialist agent.",
    sub_agents=[billing_agent, support_agent],
)
```

**Key**: When using `sub_agents`, control transfers fully to the sub-agent. The parent is out of the loop until the sub-agent finishes.

## 4. Agent-as-Tool (AgentTool)

The coordinator calls specialist agents as tools, keeping control throughout.

```python
from google.adk.tools import AgentTool

flight_agent = LlmAgent(name="FlightAgent", description="Books flights.", instruction="...")
hotel_agent = LlmAgent(name="HotelAgent", description="Books hotels.", instruction="...")

root_agent = LlmAgent(
    name="TravelPlanner",
    model="gemini-2.5-flash",
    instruction="Plan trips. Use flight_tool then hotel_tool. Combine results.",
    tools=[
        AgentTool(agent=flight_agent),
        AgentTool(agent=hotel_agent),
    ],
)
```

**Sub-agent vs AgentTool**: Sub-agents = full handoff (employee). AgentTool = on-demand call (consultant). Use AgentTool when the coordinator needs to orchestrate multi-step workflows and retain control.

## 5. Loop Agent

Repeats sub-agents until a condition is met (e.g., max iterations or an `escalate` action).

```python
from google.adk.agents import LoopAgent, LlmAgent

drafter = LlmAgent(name="Drafter", instruction="Draft or improve the essay on {topic}.", output_key="draft")
critic = LlmAgent(
    name="Critic",
    instruction="Critique {draft}. If good enough, call the 'escalate' tool to stop. Otherwise provide feedback.",
    output_key="feedback",
)

root_agent = LoopAgent(name="EssayRefiner", sub_agents=[drafter, critic], max_iterations=5)
```

## 6. Custom Orchestrator (BaseAgent)

For logic not expressible with standard workflow agents.

```python
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
from typing_extensions import override

class ConditionalAgent(BaseAgent):
    writer: LlmAgent
    reviewer: LlmAgent
    rewriter: LlmAgent

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        # Run writer
        async for event in self.writer.run_async(ctx):
            yield event

        # Check state to decide next step
        review_needed = ctx.session.state.get("needs_review", True)
        if review_needed:
            async for event in self.reviewer.run_async(ctx):
                yield event
            # Conditionally rewrite
            if ctx.session.state.get("review_passed") != "yes":
                async for event in self.rewriter.run_async(ctx):
                    yield event
```

Pass `sub_agents=[self.writer, self.reviewer, self.rewriter]` to `super().__init__()` so the framework knows about them.
