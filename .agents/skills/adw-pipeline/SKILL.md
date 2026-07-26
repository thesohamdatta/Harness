# ADW Pipeline

Architect → Developer → Reviewer multi-agent workflow using google-antigravity.

## Stages

1. **Architect** (read-only): Produces page spec from goals + DESIGN.md + reference site
2. **Developer** (full access): Builds HTML/CSS/JS from spec
3. **Reviewer** (read-only): Audits against DESIGN.md rules

## Running

```powershell
python workflows/adw-pipeline.py --all
python workflows/adw-pipeline.py --page index
```

Configs live in `prompts/` — each agent role gets its own module with `create_config()`.

Pipeline outputs (specs, reviews) go in `.scratch/adw-pipeline/`.
