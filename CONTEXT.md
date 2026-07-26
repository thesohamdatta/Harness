# Aura Website — Domain Model

## Glossary

| Term | Definition |
|---|---|
| **Aura** | Open-source, screenless, voice-first AI pendant. Worn around the neck. ~$50 BOM. MIT licensed. |
| **ADW Pipeline** | Architect → Developer → Reviewer multi-agent workflow using google-antigravity Agent class. Each role has a dedicated system prompt and tool set. |
| **Architect** | ADW role that produces page specs from goals + design system. Read-only tool access. |
| **Developer** | ADW role that builds HTML/CSS/JS from Architect specs. Full tool access. |
| **Reviewer** | ADW role that audits built pages against DESIGN.md rules. Read-only tool access. |
| **The Third Device** | Core philosophy: not a computer, not a phone, something worn. Less socially disruptive technology. |
| **Harness** | The google-antigravity Agent runtime wrapped by `agent_harness.py`. Provides CLI access, config management, and tool policy. |
| **DESIGN.md** | Design system source of truth. Apple-inspired, no shadows, frosted glass nav, accessibility-first. |
| **Reference Site** | `D:\PROJECTS\aura\website\` — the original Tailwind-based 5-page marketing site. Source of content and assets. |
| **New Site** | `D:\PROJECTS\Harness\SDK\website\` — target location for the redesigned site. |
| **Design Tokens** | CSS custom properties in `global.css` (e.g. `--color-ink`, `--type-body`). All colors and typography use tokens, never raw values. |

## Domain Rules

- All styling decisions come from DESIGN.md first. Never contradict it.
- Assets are copied from the reference site, never created from scratch.
- The harness is the runtime only — project-specific config lives in `prompts/`.
- The ADW pipeline is sequential per page: Architect → Developer → Reviewer.
- Pipeline outputs (specs, reviews) go in `.scratch/adw-pipeline/`.
