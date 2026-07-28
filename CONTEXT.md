# Aura Website — Domain Model

## Glossary

| Term                     | Definition                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Aura**                 | Open-source, screenless, voice-first AI pendant. Worn around the neck. ~$50 BOM. MIT licensed.                                                               |
| **ADW Pipeline**         | Architect → Developer → Reviewer multi-agent workflow using google-antigravity Agent class. Each role has a dedicated system prompt and tool set.            |
| **Architect**            | ADW role that produces page specs from goals + design system. Read-only tool access. Emits a strict schema spec.                                             |
| **Developer**            | ADW role that builds HTML/CSS/JS from Architect specs. Full tool access. Writes BUILD_NOTES per page.                                                        |
| **Reviewer**             | ADW role that audits built pages against an 18-rule Apple-HIG checklist. Read-only. Verdict: PASS / PASS WITH NOTES / FAIL.                                  |
| **The Third Device**     | Core philosophy: not a computer, not a phone, something worn. Less socially disruptive technology.                                                           |
| **Harness**              | The google-antigravity Agent runtime wrapped by `agent_harness.py`. Provides CLI access, config management, and tool policy.                                 |
| **BRAND_BRIEF.md**       | Design philosophy source of truth. Apple-HIG translation. Read first. Defines per-page section contracts.                                                    |
| **DESIGN.md**            | Design system source of truth. Apple-inspired, no shadows, frosted glass nav, accessibility-first. The only place raw color/typography literals are allowed. |
| **Design Tokens**        | CSS custom properties in `global.css` (e.g. `--color-ink`, `--type-body`). All colors and typography use tokens, never raw values.                           |
| **Build Target**         | `D:\PROJECTS\Harness\SDK\website\` — the redesigned site lives here.                                                                                         |
| **Re-Architect on FAIL** | Pipeline recovery mode: on Reviewer FAIL, the Architect re-runs with the review feedback appended, producing a tighter spec. Up to 3 cycles.                 |
| **Run Snapshot**         | Per-cycle audit trail at `.scratch/adw-pipeline/runs/<page>/iter-NN/<stage>/{prompt,response}.md`.                                                           |

## Domain Rules

- All styling decisions come from `BRAND_BRIEF.md` first, then `DESIGN.md`. Never contradict either.
- All assets are reused from `website/assets/` — never fabricated.
- The harness is self-contained: no path outside `D:\PROJECTS\Harness\SDK` is allowed in prompts.
- The ADW pipeline is sequential per page: Architect → Developer → Reviewer, up to 3 cycles.
- On FAIL, the next cycle re-runs Architect with feedback — never just re-Develop.
- Pipeline outputs (specs, builds, reviews, runs) go in `.scratch/adw-pipeline/`.
- System prompts read `BRAND_BRIEF.md` and `DESIGN.md` before doing anything.
