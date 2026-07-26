# Research: google-antigravity SDK & Vibe Coding SDLC

> Compiled 2026-07-26

---

## Topic 1: google-antigravity SDK (v0.1.8)

### Source: Installed package at `C:\Users\Soham\AppData\Roaming\Python\Python313\site-packages\google\antigravity\`

---

#### 1.1 Agent Class (Layer 1 API)

**File:** `agent.py`

- `Agent` is the high-level, batteries-included async context manager. It wraps config, tool runner, hook runner, trigger runner, and conversation behind a single `async with Agent(config) as agent:` entry point. (`agent.py:34-48`)
- On `__aenter__`, it registers hooks, applies policies, creates the strategy, starts the conversation, starts triggers, and wires ToolContext into tools. (`agent.py:62-146`)
- Enforces a **safety policy requirement**: write tools or MCP servers enabled without a policy raises `ValueError`. (`agent.py:93-103`)
- Exposes `chat(prompt)` -> `ChatResponse` for high-level interaction, and `conversation` property for low-level step streaming. (`agent.py:162-171, 179-193`)
- Supports session resumption via `conversation_id`. (`agent.py:195-205`)

#### 1.2 AgentConfig (Base Configuration)

**File:** `connections/connection.py`

- Abstract base combining `abc.ABC` + `pydantic.BaseModel`. Each connection strategy provides a concrete subclass. (`connection.py:38-44`)
- Key fields: `system_instructions`, `capabilities` (CapabilitiesConfig), `tools`, `policies`, `hooks`, `triggers`, `mcp_servers`, `workspaces`, `conversation_id`, `session_continuation_mode`, `save_dir`, `app_data_dir`, `response_schema`, `skills_paths`, `subagents`. (`connection.py:48-68`)
- Validates `conversation_id` (min 32 chars, alphanumeric + hyphens). (`connection.py:70-82`)
- Validates `response_schema` (JSON string, dict, or pydantic model). (`connection.py:96-113`)
- `model_copy()` overridden to NOT deep-copy callables (tools, hooks, triggers, policies) — preserving reference identity. (`connection.py:138-153`)
- Abstract `create_strategy()` factory — each config subclass returns its own ConnectionStrategy. (`connection.py:155-177`)

#### 1.3 Connection & ConnectionStrategy (Layer 3 Adapter)

**File:** `connections/connection.py`

- `Connection` is the live session contract: `send()`, `receive_steps()`, `disconnect()`, `cancel()`, `wait_for_idle()`, `wait_for_wakeup()`, `send_trigger_notification()`. (`connection.py:180-265`)
- `ConnectionStrategy` is the factory: `connect()` returns a Connection, `__aenter__`/`__aexit__` manage lifecycle. (`connection.py:268-305`)

#### 1.4 LocalAgentConfig (Default Config)

**File:** `connections/local/local_connection_config.py`

- Default config for the "local harness" (Go-based localharness binary). (`local_connection_config.py:154-166`)
- Shorthand fields: `model`, `api_key`, `vertex`, `project`, `location`. Merged into `models` list automatically. (`local_connection_config.py:169-175, 225-300`)
- Default `workspaces` = `[os.getcwd()]`. Automatically prepends `workspace_only()` policy. (`local_connection_config.py:107, 116-133`)
- Default `policies` = `policy.confirm_run_command()`. (`local_connection_config.py:97-99`)
- Wire path normalization: converts `file://` and `cns://` URIs to native paths. (`local_connection_config.py:68-84`)
- `BuiltinTools` mapped to proto fields: `CREATE_FILE`, `EDIT_FILE`, `FIND_FILE`, `LIST_DIR`, `RUN_COMMAND`, `SEARCH_DIR`, `VIEW_FILE`, `START_SUBAGENT`, `GENERATE_IMAGE`, `SEARCH_WEB`, `READ_URL_CONTENT`, `FINISH`. (`local_connection_config.py:40-53`)

#### 1.5 LocalOpenAIAgentConfig

**File:** `connections/local/local_openai_connection_config.py`

- For **any external OpenAI-compatible API** (Ollama, LM Studio). (`local_openai_connection_config.py:29-30`)
- Fields: `model` (str or ModelTarget), `base_url`. (`local_openai_connection_config.py:32-37`)
- Default capabilities: all tools enabled (file_reads, file_writes, command_execution, subagents, mcp). (`local_openai_connection_config.py:66-73`)
- Uses `LocalOpenAIConnectionStrategy` under the hood. (`local_openai_connection_config.py:99-117`)

#### 1.6 LiteRTAgentConfig

**File:** `connections/local/litert_connection_config.py`

- For **local Gemma models** via LiteRT-LM PyPI backend. (`litert_connection_config.py:36-37`)
- Fields: `model_path` (required), `backend` (CPU/GPU/NPU), `enable_speculative_decoding`, `cache_dir`, `audio_backend`, `vision_backend`, `port`, `download_if_missing`, `max_context_tokens`. (`litert_connection_config.py:39-75`)
- Default backend: GPU. Default capabilities: all tools enabled. (`litert_connection_config.py:43-44, 114-121`)
- Uses `LiteRTConnectionStrategy`. (`litert_connection_config.py:142-164`)

#### 1.7 Policy System

**File:** `hooks/policy.py`

- Declarative tool-call policies: `APPROVE`, `DENY`, `ASK_USER`. (`policy.py:101-106`)
- **Priority hierarchy**: Specific Deny > Specific Ask > Specific Allow > Wildcard Deny > Wildcard Ask > Wildcard Allow. First match wins within each group. (`policy.py:21-24, 542-554`)
- Builder functions: `allow(tool)`, `deny(tool)`, `ask_user(tool, handler=)`, `allow_all()`, `deny_all()`, `confirm_run_command()`, `safe_defaults(handler)`, `workspace_only(paths)`. (`policy.py:222-535`)
- **MCP-aware policies**: `"server/*"` prefix wildcards and `"server/tool"` exact matches. (`policy.py:598-611`)
- `enforce(policies)` creates a `_PolicyDecideHook` bucketed by priority. (`policy.py:836-886`)
- **Fail-closed**: exceptions during policy evaluation deny the tool call. (`policy.py:718-730, 751-758`)
- Predicates support pydantic model validation of tool args for type-safe matching. (`policy.py:644-651`)
- `workspace_only()` uses canonicalized path comparison with case-insensitive fs detection. (`policy.py:509-535`)

#### 1.8 Conversation (Layer 2 Session)

**File:** `conversation/conversation.py`

- Stateful session wrapping a Connection. Accumulates step history with compaction tracking. (`conversation.py:47-52`)
- `chat(prompt)` -> `ChatResponse` — unified send + stream. (`conversation.py:206-222`)
- `send()` + `receive_steps()` for low-level turn control. Auto-drains in-progress turns. (`conversation.py:106-155`)
- `receive_chunks()` yields typed `Thought`, `Text`, or `ToolCall` events. (`conversation.py:157-193`)
- History introspection: `history`, `last_response`, `turn_count`, `compaction_indices`, `total_usage`. (`conversation.py:228-331`)
- Max history size limit (default 10,000 steps) with trimming. (`conversation.py:57-58, 273-288`)

#### 1.9 ToolContext

**File:** `tools/tool_context.py`

- Conversation-aware context injected into tools that declare a `ToolContext`-typed parameter. (`tool_context.py:41-51`)
- Exposes `conversation_id` and per-conversation state store (`get_state`, `set_state`, `update_state`). Thread-safe via `threading.RLock`. (`tool_context.py:66-69, 41-51`)
- Model never sees the ToolContext parameter — schema generation strips it automatically. (`tool_context.py:24-25`)

#### 1.10 ToolRunner

**File:** `tools/tool_runner.py`

- Registry and executor for in-process Python tools. Registration-time signature inspection caches ToolContext injection points. (`tool_runner.py:142-190`)
- Auto-injects ToolContext at execution time if the tool declares the parameter. (`tool_runner.py:251-270`)
- Pydantic-based type coercion of arguments to match function annotations. (`tool_runner.py:272-311`)
- Batch execution via `process_tool_calls()` with concurrent `asyncio.gather`. Errors return ToolResult with error, don't raise. (`tool_runner.py:337-377`)

#### 1.11 Hook System

**File:** `hooks/hooks.py`

- Three hook types: `InspectHook` (read-only), `DecideHook` (blocking policy), `TransformHook` (modifying). (`hooks.py:70-118`)
- Lifecycle hooks: `OnSessionStartHook`, `OnSessionEndHook`, `PreTurnHook`, `PostTurnHook`, `PreToolCallDecideHook`, `PostToolCallHook`, `OnToolErrorHook`, `OnInteractionHook`, `OnCompactionHook`. (`hooks.py:124-218`)
- Decorator factory: `@hooks.pre_turn`, `@hooks.pre_tool_call_decide`, `@hooks.post_tool_call`, etc. (`hooks.py:224-268`)
- Context hierarchy: `SessionContext` > `TurnContext` > `OperationContext`. (`hooks.py:35-61`)

#### 1.12 Types

**File:** `types.py`

- `BuiltinTools` enum: `LIST_DIR`, `SEARCH_DIR`, `FIND_FILE`, `VIEW_FILE`, `CREATE_FILE`, `EDIT_FILE`, `RUN_COMMAND`, `ASK_QUESTION`, `START_SUBAGENT`, `GENERATE_IMAGE`, `SEARCH_WEB`, `READ_URL_CONTENT`, `FINISH`. Grouped into `read_only()`, `nondestructive()`, `file_tools()`, `all_tools()`, `none()`. (`types.py:189-293`)
- `CapabilitiesConfig`: `enable_subagents`, `enabled_tools`/`disabled_tools` (mutually exclusive), `compaction_threshold`, `finish_tool_schema_json`. (`types.py:295-345`)
- `Step` model: `id`, `step_index`, `type`, `source`, `target`, `status`, `content`, `thinking`, `content_delta`, `thinking_delta`, `tool_calls`, `error`, `is_complete_response`, `structured_output`, `usage_metadata`. (`types.py:596-637`)
- `ChatResponse`: async streaming with independent cursors for `chunks`, `thoughts`, `tool_calls`. Supports `text()`, `structured_output()`, `usage_metadata`, `cancel()`. (`types.py:812-951`)
- `Content` = `str | Image | Document | Audio | Video | SlashCommand | Sequence[ContentPrimitive]`. (`types.py:1144-1145`)
- MCP configs: `McpStdioServer` (stdio) and `McpStreamableHttpServer` (HTTP), both with `enabled_tools`/`disabled_tools`. (`types.py:376-435`)

#### 1.13 GitHub Repo

**URL:** https://github.com/Google-Antigravity/antigravity-sdk-python

- 2.6k stars, 998 forks, 401 commits. Apache 2.0 license.
- Three-layer architecture: Layer 1 (Agent) -> Layer 2 (Conversation) -> Layer 3 (Connection).
- Components: Agent, Connections, Conversation, Hooks, MCP integration, Tools, Triggers.
- Requires compiled Go-based localharness binary shipped via PyPI platform-specific wheels.

---

## Topic 2: Vibe Coding & New SDLC Patterns

---

### 2.1 Definition & Origin

**Source:** Wikipedia, Google Cloud, GitHub resources

- **Vibe coding** is a natural-language-driven, AI-assisted workflow where you describe goals and iteratively guide AI agents rather than writing every line of code yourself.
- Term coined by **Andrej Karpathy** in early 2025. Originally described as "letting AI generate code while you half-watch, accepting what works."

### 2.2 Google's Whitepaper: "The New SDLC With Vibe Coding"

**Source:** Kaggle whitepaper by Addy Osmani, Shubham Saboo, Sokratis Kartakis (June 2026, ~50 pages)

**Five central arguments:**

1. **Agent = Model + Harness** — The model is ~10% of the equation. The other 90% is the harness: instructions, tools, MCP servers, sandboxes, orchestration logic, guardrails, observability. *"The same model can score 15 points apart on the same benchmark depending on which agent harness wraps it."* (TensorFeed.ai)
2. **The SDLC compresses unevenly** — Implementation drops from weeks to hours. Requirements, architecture, and verification stay slow (they are judgment work). Verification is the new bottleneck.
3. **The economics invert at scale** — Vibe coding is cheap up front (subscription), expensive to run (token burn, maintenance tax from ad-hoc code, security cleanup). Past the crossover point, vibe coding costs 3-10x more per feature than agentic engineering.
4. **Verification is the binding constraint** — Generation is largely solved. The hard problem is knowing whether output is correct. SonarSource: only 48% of developers consistently check AI code before committing; 38% find reviewing AI code harder than human-written code.
5. **Generator-evaluator split** — Anthropic's solution: a separate skeptical agent grades the generator's output. Agents built a working C compiler in Rust over two weeks with this architecture.

### 2.3 The Vibe Coding Spectrum

| Mode | Description | Best For |
|------|-------------|----------|
| **Vibe Coding** | Casual prompts, "does it seem to work?", minimal codebase understanding | Prototypes, scripts, hackathons |
| **Structured AI-assisted** | Detailed prompts with constraints, manual testing, selective review | Features in established codebases |
| **Agentic Engineering** | Formal specs, architecture docs, evals, CI/CD gates, LLM judges | Production systems at team scale |

### 2.4 The "Harness" Concept in AI Coding

**Source:** TensorFeed.ai (harness leaderboard), MindStudio (Cursor SDK vs Claude Code harness), Requesty (agent harness as infrastructure layer)

- **The harness is now the critical variable.** Claude Opus 4.7 scores 87.2% in Claude Code's harness vs 91.1% in Cursor's harness on the same benchmark (Endor Labs). The harness gap (3.9 pts) exceeds typical model generation gaps.
- **Sam Altman (OpenAI CEO):** "Hard to overstate how critical [the harness] is. I no longer think of the harness and the model as these entirely separable things."
- Nine components of a serious agent harness: the while-loop (outer iteration engine), context management, skills and tools, sub-agent management, built-in skills, session persistence, system prompt assembly, lifecycle hooks, permissions and safety.
- **Harness-as-a-service** is an emerging category: Cursor SDK, Claude managed agents, OpenAI Agents SDK, Microsoft hosted agents in Foundry.

### 2.5 The New SDLC Phases (AI-Augmented)

| Phase | What Changes |
|-------|-------------|
| **Requirements** | A conversation producing a spec and prototype simultaneously |
| **Architecture** | "The most stubbornly human phase" — trade-offs need context models lack |
| **Implementation** | 25-39% gains per surveys. METR: devs go 19% *slower* on some tasks counting review time |
| **Testing & QA** | Evals become the primary way to tell the agent what "correct" means |
| **Maintenance** | Code "too risky to touch" can now be refactored by agents |

### 2.6 Context Engineering

- Replaces "prompt engineering" as the core competency.
- Six kinds of context: **instructions** (role and boundaries), **knowledge** (docs, diagrams, domain data), **memory** (session logs + long-term project state), **examples** (reference patterns), **tools** (APIs and scripts), **guardrails** (hard constraints and safety rules).
- Key design decision: **static** vs **dynamic** context. Static is always loaded (reliable but expensive). Dynamic is loaded on demand via Agent Skills (efficient).

### 2.7 Key Players in 2026

| Tool | Type | Key Strength |
|------|------|-------------|
| **Claude Code** | CLI Agent | #1 ranked, autonomous multi-file ops, deep codebase context |
| **Cursor 3** | IDE Agent | Parallel agents, cloud VMs, TypeScript SDK for orchestration |
| **OpenAI Codex** | CLI/Cloud | Async workhorse, background PRs |
| **Google Antigravity** | Agent Platform | Full agentic dev platform, MCP, policy system, local/cloud/on-device |
| **Gemini CLI** | CLI | Open-source terminal-first agent |
| **Devin 2** | Agent Platform | Autonomous issue-to-PR pipeline |

---

## Practical Patterns for a Dev Harness with google-antigravity SDK

### Pattern 1: Safety-First Agent with Workspace Sandboxing

```python
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

config = LocalAgentConfig(
    system_instructions="You are a coding assistant.",
    capabilities=CapabilitiesConfig(enable_subagents=True),
    workspaces=["D:/PROJECTS/Harness/SDK"],
    # run_command is denied by default via confirm_run_command()
)
async with Agent(config) as agent:
    response = await agent.chat("Refactor the utils module.")
```

**Key SDK features used:** `workspaces` auto-scoping via `policy.workspace_only()`, default `confirm_run_command()` policy, auto-generated policy rules.

### Pattern 2: Policy-Driven Approval Flow

```python
from google.antigravity.hooks.policy import deny, allow, ask_user

async def my_approval_handler(tool_call):
    print(f"Approve {tool_call.name}({tool_call.args})? [y/N] ")
    return input().lower() == "y"

policies = [
    deny("*"),
    allow("view_file"),
    allow("list_directory"),
    allow("search_directory"),
    allow("find_file"),
    allow("read_url_content"),
    ask_user("run_command", handler=my_approval_handler),
    ask_user("edit_file", handler=my_approval_handler),
    ask_user("create_file", handler=my_approval_handler),
]
```

**Key SDK features used:** Priority-based policy evaluation (`policy.py:542-554`), `ask_user` with custom handlers, `deny("*")` as default-deny posture.

### Pattern 3: Custom Tools with ToolContext

```python
from google.antigravity.tools.tool_context import ToolContext

def search_codebase(query: str, ctx: ToolContext) -> str:
    """Search the codebase for a pattern."""
    last = ctx.get_state("last_search")
    ctx.set_state("last_search", query)
    return f"Results for '{query}' (previous: {last})..."
```

**Key SDK features used:** ToolContext auto-injection (`tool_runner.py:251-270`), per-session state store, parameter stripped from model schema.

### Pattern 4: Lifecycle Hook for Observability

```python
from google.antigravity.hooks import hooks as hooks_mod

@hooks_mod.pre_tool_call_decide
async def log_tool_call(data):
    print(f"Tool called: {data.name} args={data.args}")

@hooks_mod.post_turn
async def log_response(data):
    print(f"Turn completed: {len(data)} chars")
```

**Key SDK features used:** Decorator-based hook registration, lifecycle hierarchy (session/turn/operation), `InspectHook` for non-blocking observability.

### Pattern 5: MCP-Connected Agent

```python
from google.antigravity.types import McpStdioServer

config = LocalAgentConfig(
    mcp_servers=[
        McpStdioServer(
            name="filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
        ),
    ],
    # MCP requires explicit policy — will raise ValueError without one
    policies=[policy.allow_all()],
)
```

**Key SDK features used:** `McpStdioServer` config, MCP-aware policy matching via `"server/*"` prefix, safety guard that requires policies when MCP is enabled.

### Pattern 6: Interactive Loop with Streaming

```python
async with Agent(config) as agent:
    response = await agent.chat("Explain the architecture.")
    async for token in response:
        sys.stdout.write(token)
        sys.stdout.flush()
    # Also stream thoughts
    async for thought in response.thoughts:
        ...
    # Intercept tool calls in real-time
    async for tool_call in response.tool_calls:
        ...
```

**Key SDK features used:** `ChatResponse` multi-cursor streaming (`types.py:812-951`), independent `chunks`, `thoughts`, `tool_calls` streams.

### Pattern 7: Low-Level Conversation Control

```python
from google.antigravity.conversation.conversation import Conversation
from google.antigravity.connections.local import LocalConnectionStrategy

strategy = LocalConnectionStrategy(tool_runner=ToolRunner())
async with Conversation.create(strategy) as conv:
    await conv.send("List all files.")
    async for step in conv.receive_steps():
        if step.is_complete_response:
            print(f"[{step.type}] {step.content}")
    print(f"Tokens used: {conv.total_usage}")
```

**Key SDK features used:** Direct `Conversation` usage, step-by-step streaming, usage tracking, history accumulation.

### Pattern 8: Subagent Delegation

```python
from google.antigravity.types import SubagentConfig, SubagentCapabilities, BuiltinTools

config = LocalAgentConfig(
    subagents=[
        SubagentConfig(
            name="code_reviewer",
            description="Reviews code changes for quality",
            system_instructions="You are a strict code reviewer.",
            capabilities=SubagentCapabilities(
                enabled_tools=BuiltinTools.read_only()
            ),
        )
    ],
)
```

**Key SDK features used:** `SubagentConfig` with per-subagent tool allowlists, `start_subagent` builtin tool, subagent capabilities isolation.

---

## Vibe-Coding SDLC Pattern Summary

### The Core Insight

The new SDLC is not about replacing developers — it's about **moving the bottleneck from implementation to specification and verification**. The Google whitepaper's central equation:

```
Agent = Model (~10%) + Harness (~90%)
```

### The Five SDLC Shifts

1. **Requirements become conversational** — A spec and prototype emerge simultaneously from dialogue.
2. **Architecture stays human** — The most stubbornly human phase; trade-off decisions need context models lack.
3. **Implementation accelerates 3-10x** — But the savings are consumed by verification costs.
4. **Testing becomes evals** — Automated test suites + LLM judges replace manual QA as the primary quality gate.
5. **Maintenance gets unblocked** — Legacy code frozen by bus-factor risk can now be modernized by agents.

### The Verification Bottleneck

- Only 48% of developers consistently check AI-generated code (SonarSource).
- 38% find reviewing AI code harder than human-written code.
- Agents evaluating their own work "reliably skew positive" (Anthropic).
- **Solution:** Generator-evaluator split — separate skeptical agent that grades output.

### Context Engineering as the New Craft

Six context types to manage deliberately:

| Type | Examples | Load Strategy |
|------|----------|---------------|
| Instructions | Role, boundaries, rules | Static (AGENTS.md) |
| Knowledge | Docs, diagrams, specs | Dynamic (retrieval) |
| Memory | Session logs, long-term state | Hybrid |
| Examples | Reference patterns | Dynamic (on-demand) |
| Tools | APIs, scripts, MCP servers | Static |
| Guardrails | Hard constraints, safety rules | Static |

### Developer Role Evolution

**Before:** Write code -> Review -> Deploy
**After:** Specify intent -> Verify output -> Orchestrate agents

Two operating modes identified:
- **The Conductor** — Real-time, in-IDE, tight feedback loop (Cursor, Claude Code)
- **The Orchestrator** — Async, goal-driven, delegates to background agents (Codex, Devin)

### The Harness Landscape (2026)

| Harness | Type | SWE-bench Score (top) | Key Differentiator |
|---------|------|-----------------------|---------------------|
| Claude Code | CLI | 74.5% | Deep context, subagents |
| Codex CLI | CLI | 72.8% | Async cloud execution |
| Cursor Agent | IDE | 70.1% | Parallel agents, SDK |
| OpenHands | Platform | 65.8% | Open-source, extensible |

The **google-antigravity SDK** fits as a programmable harness — not an end-user tool like Claude Code, but a **Python library for building custom coding agents** with fine-grained control over policy, tools, hooks, triggers, MCP, and conversation lifecycle. Its three-layer architecture (Agent -> Conversation -> Connection) mirrors the industry-standard harness components.
