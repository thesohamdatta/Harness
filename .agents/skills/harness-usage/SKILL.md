# Harness Usage

The google-antigravity harness wraps the Agent class for CLI-driven interactions.

## Entry points
- `agent_harness.py` — general CLI agent (--aura, --read-only, --workspace flags)
- `prompts/aura.py` — Aura-specific config (direct import or via `python -m prompts.aura`)
- `workflows/adw-pipeline.py` — multi-agent pipeline runner

## Config pattern
Each agent module exports `create_config()` returning `LocalAgentConfig`:
```python
def create_config() -> LocalAgentConfig:
    return LocalAgentConfig(
        model="gemini-3.6-flash",
        system_instructions=SYSTEM_INSTRUCTIONS,
        workspaces=[...],
        capabilities=...,
    )
```

## Environment
- `GEMINI_API_KEY` must be set
- All interactions are async (`asyncio.run()`)
