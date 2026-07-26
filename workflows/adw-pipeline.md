# ADW Pipeline: Architect → Developer → Reviewer

The ADW pipeline is a multi-agent workflow that builds website pages through three
coordinated agent roles. Each role gets a dedicated Agent with its own system prompt
and tool capabilities.

## Stages

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Architect │ ──> │ Developer│ ──> │ Reviewer │
│ (plan)    │     │ (build)  │     │ (audit)  │
└──────────┘     └──────────┘     └──────────┘
```

### 1. Architect (plans)
- Input: Project goals, DESIGN.md, reference site
- Output: Page spec (markdown) per page
- Tools: Read-only (read files, no edits)

### 2. Developer (builds)
- Input: Page spec from Architect
- Output: HTML/CSS/JS files
- Tools: Full (read + write files)

### 3. Reviewer (audits)
- Input: Built page files + DESIGN.md
- Output: Review report (PASS/FAIL)
- Tools: Read-only

## Running the pipeline

```powershell
python workflows\adw-pipeline.py --page index
python workflows\adw-pipeline.py --page manifesto
python workflows\adw-pipeline.py --page docs
python workflows\adw-pipeline.py --all         # all pages sequentially
```

## Pipeline config

- Model: gemini-3.6-flash (all roles)
- Workspaces: website/, reference site, harness SDK root
- API key from GEMINI_API_KEY env var

## Output artifacts

- `.scratch/adw-pipeline/specs/` — Architect specs
- `.scratch/adw-pipeline/reviews/` — Reviewer reports
- `website/` — built page files
