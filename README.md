# 🤖 Building Google ADK Agents — Claude Agent Skill

A [Claude Agent Skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) that teaches Claude how to build AI agents using [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/). When this skill is active, Claude can scaffold complete ADK projects, write well-structured tools, configure multi-agent systems, manage session state, and guide you through deployment — all following ADK best practices.

## What This Skill Does

When you ask Claude things like:

- *"Build me an ADK agent that can search the web and summarize results"*
- *"Create a multi-agent pipeline that drafts, reviews, and refines code"*
- *"Set up an ADK agent with session state that remembers user preferences"*

Claude will generate correct, runnable ADK code — including proper project structure, function tools with complete docstrings, state management with `ToolContext`, and appropriate agent types (`LlmAgent`, `SequentialAgent`, `ParallelAgent`, etc.).

## Topics Covered

| Area | What Claude Learns |
|------|-------------------|
| **Agent Types** | `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, custom `BaseAgent` |
| **Function Tools** | Proper docstrings, type hints, dict returns, `ToolContext` for state access |
| **Multi-Agent Patterns** | Sequential pipelines, parallel fan-out, LLM delegation, `AgentTool`, custom orchestrators |
| **Sessions & State** | `InMemorySessionService`, state key prefixes (`user:`, `app:`, `temp:`), instruction templating |
| **Memory** | `InMemoryMemoryService`, `VertexAiMemoryBankService`, `load_memory` / `PreloadMemory` tools |
| **Callbacks** | All 6 callback types — guardrails, auth checks, logging, output modification |
| **Running & Deploying** | `InMemoryRunner`, `adk web` / `adk run` CLI, Cloud Run, Vertex AI Agent Engine |

## Installation

### Option A: Claude Code (Recommended)

From the root of your project, run:

```bash
claude skill add /path/to/google-adk-skill
```

Or if you've cloned this repo:

```bash
claude skill add ./google-adk-skill
```

### Option B: Manual Installation

1. Clone this repository:

```bash
git clone https://github.com/YOUR_USERNAME/google-adk-skill.git
```

2. Copy the skill folder into your Claude skills directory. The exact location depends on your setup:

```bash
# For Claude Code project-level skills:
cp -r google-adk-skill /path/to/your/project/.claude/skills/

# For Claude Code user-level skills:
cp -r google-adk-skill ~/.claude/skills/
```

3. Claude will automatically discover the skill via the `SKILL.md` frontmatter when it's relevant to your request.

### Option C: API / Agent SDK Usage

If you're using the [Anthropic API with Skills](https://docs.anthropic.com/en/docs/build-with-claude/skills-guide), upload the entire `google-adk-skill/` directory as a skill resource. Claude will read `SKILL.md` when ADK-related tasks are detected and load reference files on demand.

## Repository Structure

```
google-adk-skill/
├── SKILL.md                                # Main skill file (entry point Claude reads first)
├── README.md                               # This file
├── reference/
│   ├── multi-agent-patterns.md             # 6 patterns: Sequential, Parallel, Loop, AgentTool, etc.
│   ├── sessions-and-state.md               # State prefixes, session services, memory services
│   ├── callbacks.md                        # All callback types with practical examples
│   ├── running-and-deploying.md            # Runner setup, CLI, Cloud Run, Vertex AI
│   └── evaluations.md                      # Test scenarios to validate skill effectiveness
├── templates/
│   ├── agent_template.py                   # Single agent with tools + ToolContext state access
│   └── multi_agent_template.py             # SequentialAgent + ParallelAgent pipeline
└── scripts/                                # Reserved for future utility scripts
```

### How Progressive Disclosure Works

Claude doesn't load everything at once. The architecture is designed to be token-efficient:

1. **Always loaded**: Only the `name` and `description` from `SKILL.md` frontmatter (used for skill discovery)
2. **Loaded on trigger**: The body of `SKILL.md` — when Claude detects an ADK-related task
3. **Loaded on demand**: Reference files (e.g., `reference/callbacks.md`) — only when the specific topic comes up
4. **Executed, not loaded**: Template files can be copied/adapted without consuming context tokens

## Quick Verification

After installing, test the skill with a prompt like:

> "Create a Google ADK agent that looks up stock prices and saves the user's favorite ticker to session state."

Claude should produce:
- A proper project structure (`agent.py`, `__init__.py`, `.env`)
- Function tools with full docstrings and type hints
- `ToolContext` usage for state management
- A `root_agent` variable with clear instructions
- A valid model string (e.g., `gemini-2.5-flash`)

## Customization

### Adding More Reference Material

Create new `.md` files in `reference/` and add a link from `SKILL.md`:

```markdown
### My New Topic

See [reference/my-new-topic.md](reference/my-new-topic.md) for:
- Detail 1
- Detail 2
```

Keep references one level deep from `SKILL.md` — avoid chains like `SKILL.md → A.md → B.md`.

### Adding Templates

Drop new `.py` files into `templates/`. Reference them in `SKILL.md` if Claude should know about them, or leave them as passive resources for users to copy.

### Updating for New ADK Versions

The skill is based on ADK Python v1.x (`google-adk` on PyPI). When ADK releases new features:

1. Update the relevant reference file (e.g., new agent type → `multi-agent-patterns.md`)
2. Keep `SKILL.md` under 500 lines — split into new reference files if needed
3. Run the evaluation scenarios in `reference/evaluations.md` to verify correctness

## Skill Authoring Principles

This skill follows the [Claude Agent Skill best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices):

- **Concise**: Assumes Claude already knows Python, async patterns, and general LLM concepts — only teaches ADK-specific knowledge
- **Progressive disclosure**: `SKILL.md` is the overview; deep dives live in `reference/` files loaded on demand
- **One level deep**: All reference files link directly from `SKILL.md`, no nested chains
- **Consistent terminology**: Always "tool" (not "function"), "state" (not "context data"), "instruction" (not "prompt")
- **No time-sensitive info**: No version-specific dates or "use X before August 2025" patterns
- **Tested**: Includes evaluation scenarios in `reference/evaluations.md`

## Contributing

PRs welcome! If you'd like to improve this skill:

1. Fork the repo
2. Make changes following the [skill authoring best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
3. Test with the eval scenarios in `reference/evaluations.md`
4. Submit a PR with a description of what changed and why

## License

MIT — use freely in your own projects and skill collections.

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python SDK (GitHub)](https://github.com/google/adk-python)
- [Claude Agent Skills Overview](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Claude Skill Authoring Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
