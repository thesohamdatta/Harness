# Harness SDK

Google Antigravity SDK harness for AI-assisted development. Wraps the `Agent` class to provide a CLI coding assistant with configurable workspaces, multi-agent ADW pipelines, and local skills.

## What this repo is

- **`agent_harness.py`** — CLI entry point for running coding agents
- **`workflows/adw-pipeline.py`** — Architect → Developer → Reviewer multi-agent pipeline
- **`prompts/`** — System prompt builders for each ADW role
- **`.opencode/`** — OpenCode subagents and commands
- **`website/`** — Aura open-source AI pendant marketing site (redesign target)
- **`.agents/skills/`** — Local agent skills (design, pipeline, prompt engineering)

## Quick start

```powershell
$env:GEMINI_API_KEY = "your-key-here"
python agent_harness.py -w . --read-only "list all files"
```

## Website

The `website/` directory contains the redesigned Aura marketing site — 4 pages (index, manifesto, docs, 404), built with vanilla HTML/CSS/JS, Apple HIG-inspired design system from `DESIGN.md`.

## Stack

| Layer           | Technology                                  |
| --------------- | ------------------------------------------- |
| Harness runtime | google-antigravity Python SDK               |
| Agents          | local `Agent` subclasses with tool policies |
| Website         | Vanilla HTML/CSS/JS (no build, no Tailwind) |
| Design system   | Apple HIG-inspired, CSS custom properties   |

MIT licensed.
