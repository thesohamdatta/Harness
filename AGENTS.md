# Harness SDK

Google Antigravity SDK harness for AI-assisted development. Wraps the `Agent` class
to provide a CLI coding assistant with configurable workspaces, multi-agent ADW pipelines,
and local skills.

## Entry points

```powershell
$env:GEMINI_API_KEY = "AQ.Ab8RN6..."
python agent_harness.py --aura "add an FAQ section"
python agent_harness.py -w . --read-only "list all files"
python workflows/adw-pipeline.py --all              # Run full ADW pipeline
python workflows/adw-pipeline.py --page index        # Run one page
```

## Prerequisites

- `GEMINI_API_KEY` env var required at runtime
- `protobuf` >= 7.35.x (upgraded from 5.29 to match `google-antigravity` SDK dependency)

## Architecture

```
agent_harness.py              # CLI harness (entry point)
prompts/
  __init__.py                 # package marker
  aura.py                     # Aura-specific project config + system instructions
  architect.py                # ADW Architect agent config
  developer.py                # ADW Developer agent config
  reviewer.py                 # ADW Reviewer agent config
workflows/
  adw-pipeline.py             # Multi-agent pipeline orchestrator
  adw-pipeline.md             # Pipeline documentation
.agents/
  skills/
    aura-design/              # Aura design system skill
    adw-pipeline/             # ADW pipeline skill
    harness-usage/            # Harness usage skill
docs/
  agents/
    issue-tracker.md          # Local markdown issue tracker config
  research.md                 # SDK reference patterns
.scratch/
  adw-pipeline/
    specs/                    # Architect output specs
    reviews/                  # Reviewer audit reports
  wayfinder-aura-website/
    map.md                    # Wayfinder map for the redesign effort
    tickets/                  # Wayfinder tickets
CONTEXT.md                    # Domain model glossary
NOTES.md                      # raw dev-loop notes
```

- ADW pipeline: Architect (plans) → Developer (builds) → Reviewer (audits)
- Each role gets its own `LocalAgentConfig` with tailored system prompts
- Pipeline outputs to `.scratch/adw-pipeline/`
- Local skills in `.agents/skills/` for agentic reference

## Agent roles

| Role | Tools | Output |
|---|---|---|
| Architect | Read-only | Page spec markdown |
| Developer | Full (read/write) | HTML/CSS/JS files |
| Reviewer | Read-only | Audit report |

## Known quirks

- **Aura workspace path** is hardcoded to `D:\PROJECTS\aura\website` — change it in
  `prompts/aura.py` if working on another machine.
- **No tests exist.** Run `python -c "from google.antigravity import Agent"` to verify
  SDK imports resolve without protobuf version errors.
- **Async-only.** All agent interactions use `asyncio` — must be inside `async def`.
- `--model`, `--workspace`, and `--system` flags are silently ignored when `--aura` is active.
- Lazy imports: `prompts.aura` is imported only at runtime when `--aura` is used (not at
  module load time).
- ADW pipeline requires all three prompt modules to import cleanly.

## Prompt Engineering

System prompts use `prompts.engineer` - a structured builder encoding Anthropic's 2026
best practices:
  - XML-tagged sections (`<role>`, `<context>`, `<references>`, `<instructions>`, `<output>`)
  - Long context at top, instructions at bottom
  - Positive instructions over prohibitions
  - Minimal boilerplate - modern models are over-constrained
  - Progressive disclosure via `<references>` pointing to files

Debug: `python agent_harness.py --show-prompt --aura`

## Design rules

- Keep system instructions as Python string constants or external `.md` files - no templates.
- One `create_config()` per project config, all returning `LocalAgentConfig`.
- CLI flags in `agent_harness.py` should be generic (harness-level), not project-specific.
- CONTEXT.md is the domain glossary - no implementation details.
- Wayfinder maps live in `.scratch/<effort>/`.
- Prompts use `prompts.engineer.build_prompt()` for consistent XML-tagged structure.
