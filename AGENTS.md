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
python workflows/adw-pipeline.py --page index       # Run one page
python workflows/adw-pipeline.py --all --dry-run    # Plan only, no API calls
```

## Prerequisites

- `GEMINI_API_KEY` env var required at runtime
- `protobuf` >= 7.35.x (upgraded from 5.29 to match `google-antigravity` SDK dependency)

## Architecture

```
agent_harness.py              # CLI harness (entry point)
.opencode/
  opencode.json               # Project-level OpenCode config
  agent/
    builder.md                # Web builder subagent
    designer.md               # Design audit subagent
    reviewer.md               # Quality review subagent
  command/
    build-page.md             # Build one page via ADW pipeline
    build-all.md              # Build all pages via ADW pipeline
    design-audit.md           # Full site design audit
    harness.md                # Run the Google Antigravity harness
prompts/
  __init__.py                 # package marker
  aura.py                     # Single-shot Aura dev config
  architect.py                # ADW Architect system prompt
  developer.py                # ADW Developer system prompt
  reviewer.py                 # ADW Reviewer system prompt (18-rule audit)
  engineer.py                 # Prompt builder (XML-tagged)
workflows/
  adw-pipeline.py             # Architect → Developer → Reviewer with re-Architect on FAIL
  adw-pipeline.md             # Pipeline documentation
.agents/
  skills/
    aura-design/              # Aura design system skill
    adw-pipeline/             # ADW pipeline skill
    apple-hig/                # Apple HIG distilled reference
    aura-design-system/       # Skill snapshot
    harness-usage/            # Harness usage skill
    prompt-engineering/       # Prompt engineering skill
docs/
  agents/
    issue-tracker.md          # Local markdown issue tracker config
  research.md                 # SDK reference patterns
.scratch/
  adw-pipeline/
    specs/                    # Architect output specs (latest)
    reviews/                  # Reviewer audit reports (latest)
    builds/                   # Developer build notes
    runs/                     # Per-cycle snapshots (audit trail)
  wayfinder-aura-website/
    map.md                    # Wayfinder map for the redesign effort
    tickets/                  # Wayfinder tickets
CONTEXT.md                    # Domain model glossary
NOTES.md                      # raw dev-loop notes
BRAND_BRIEF.md                # Design philosophy + per-page contracts (Apple-HIG translation)
DESIGN.md                     # Design tokens (the only place raw literals live)
```

### Pipeline architecture (ADW)

ADW pipeline: Architect (plans) → Developer (builds) → Reviewer (audits), up to 3 cycles.

- Each role gets a dedicated `LocalAgentConfig` with a tailored system prompt
- Pipeline outputs to `.scratch/adw-pipeline/` (specs, builds, reviews, run snapshots)
- Local skills in `.agents/skills/` for agentic reference
- **On Reviewer FAIL, Architect re-runs with the review feedback appended** — the spec
  gets refined, not just the build re-attempted
- Run snapshots under `.scratch/adw-pipeline/runs/<page>/iter-NN/{architect,developer,reviewer}/`
  preserve every prompt + response for audit
- Summary printed at end when running --all

## Agent roles

### ADW Pipeline (via python workflows/adw-pipeline.py)

| Role      | Tools      | Output                                                                                         |
| --------- | ---------- | ---------------------------------------------------------------------------------------------- |
| Architect | Read       | Strict schema markdown spec at `.scratch/adw-pipeline/specs/<page>.md`                         |
| Developer | Full (r/w) | HTML file at `website/<page>.html` + BUILD_NOTES at `.scratch/adw-pipeline/builds/<page>.md`   |
| Reviewer  | Read       | 18-rule audit at `.scratch/adw-pipeline/reviews/<page>.md` with verdict + design fidelity note |

### OpenCode subagents (via /command)

| Agent    | Tools        | Use for                                       |
| -------- | ------------ | --------------------------------------------- |
| builder  | Full (r/w/b) | Building or editing pages                     |
| designer | Read-only    | Design audits against BRAND_BRIEF + DESIGN.md |
| reviewer | Read-only    | Quality + accessibility checks                |

## Known quirks

- **Self-contained.** No external `D:\PROJECTS\aura\website` dependency — the harness reads
  `BRAND_BRIEF.md` + `DESIGN.md` at SDK root and the in-tree `website/`. Agents must
  never reference paths outside the SDK.
- **No tests exist.** Run `python -c "from google.antigravity import Agent"` to verify
  SDK imports resolve without protobuf version errors.
- **Async-only.** All agent interactions use `asyncio` — must be inside `async def`.
- `--model`, `--workspace`, and `--system` flags are silently ignored when `--aura` is active.
- Lazy imports: `prompts.aura` is imported only at runtime when `--aura` is used.
- ADW pipeline requires all prompt modules to import cleanly.
- Re-architect-on-fail uses `iter-NN` snapshot folders so the conversation history is preserved.

## Prompt Engineering

System prompts use `prompts.engineer` — a structured builder encoding Anthropic's 2026
best practices:

- XML-tagged sections (`<role>`, `<context>`, `<references>`, `<instructions>`, `<output>`)
- Long context at top, instructions at bottom
- Positive instructions over prohibitions
- Minimal boilerplate — modern models are over-constrained
- Progressive disclosure via `<references>` pointing to files

Debug: `python agent_harness.py --show-prompt --aura`

## OpenCode commands

| Command                 | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `/build-page <page>`    | Run full ADW pipeline for one page (index/manifesto/docs) |
| `/build-all`            | Run ADW pipeline for all pages with summary report        |
| `/design-audit`         | Audit entire site against BRAND_BRIEF + DESIGN.md         |
| `/harness --aura "..."` | Run the Google Antigravity harness                        |

## Repository nesting (important)

This repo (`D:\PROJECTS\AURA\website\1.2`) is a **git submodule** inside the
parent `aura.git` at `D:\PROJECTS\AURA/`.

```
D:\PROJECTS\AURA/         ← GIT: aura.github.com/thesohamdatta/aura.git
└── website/
    └── 1.2/              ← GIT: Harness.git (this repo)
```

- **Always check** `git rev-parse --show-toplevel` before committing.
- Work on the website → commit in this repo (`website/1.2/`).
- To update the submodule pointer in parent: `git -C D:\PROJECTS\AURA add website/1.2 && git commit`
- After cloning fresh: `git submodule update --init --recursive`
- Reference: `.scratch/repo-structure-analysis.md`

## Design rules

- Brand philosophy lives in `BRAND_BRIEF.md` (read first).
- Design tokens live in `DESIGN.md` (read second; the only place raw literals live).
- System instructions as Python string constants or external `.md` files — no templates.
- One `create_config()` per project config, all returning `LocalAgentConfig`.
- CLI flags in `agent_harness.py` should be generic (harness-level), not project-specific.
- `CONTEXT.md` is the domain glossary — no implementation details.
- Wayfinder maps live in `.scratch/<effort>/`.
- Prompts use `prompts.engineer.build_prompt()` for consistent XML-tagged structure.
