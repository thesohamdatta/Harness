# Wayfinder Map: Professional Aura Website Redesign

## Destination

A redesigned, production-quality Aura website at `D:\PROJECTS\Harness\SDK\website\`, built via an ADW multi-agent pipeline using the google-antigravity harness. Three pages: home (condensed 5–6 sections), manifesto, and comprehensive docs. The reference site's core product philosophy is preserved, re-expressed in a simpler, more minimal Apple-inspired design following `DESIGN.md` strictly. Existing about.html and ai.html are removed.

## Notes

- **Design source of truth:** `D:\PROJECTS\aura\website\DESIGN.md` — Apple-inspired, no shadows, frosted glass nav, `transition-transform` only, `prefers-reduced-motion`, strict accessibility
- **Reference content:** `D:\PROJECTS\aura\website\` — all copy and assets to draw from
- **Assets:** Copy from `D:\PROJECTS\aura\website\assets\` and `D:\PROJECTS\aura\website\fonts\`
- **Existing new site:** `D:\PROJECTS\Harness\SDK\website\` has pages (index, about, ai, manifesto) + CSS/JS from previous attempts — these may be replaced or refactored
- **Issue tracker:** Local markdown per `docs/agents/issue-tracker.md`
- **Relevant skills:** `grilling`, `domain-modeling`, `frontend-design`, `design-an-interface`, `research`
- **Stack:** Vanilla HTML/CSS/JS, Tailwind CDN for utility classes, Lucide icons, SF Pro fonts

## Decisions so far

- [Set up agentic infrastructure](tickets/001--set-up-infrastructure.md) — Created ADW pipeline configs (architect, developer, reviewer), local skills (aura-design, adw-pipeline, harness-usage), CONTEXT.md, issue tracker config, and updated AGENTS.md. Pipeline imports verified clean.

## Not yet specified

- **ADW pipeline architecture:** Exact agent roles, configs, workflow orchestration — needs design before build tickets can proceed
- **Homepage section breakdown:** Which 5–6 sections exactly, and their order
- **Docs page content structure:** Specs, build guide, firmware, app — how are these organized on one page? Accordion? Tabs? Sections?
- **Manifesto page format:** Full essay? Visual essay with images? Shorter take?
- **CSS strategy:** Reuse existing global.css with design tokens, or refine? Current tokens match DESIGN.md already.
- **JS strategy:** Which JS components carry over (nav, footer, reveal, liquid-glass)?
- **Verification:** How to verify DESIGN.md compliance and visual correctness

## Out of scope

- Any pages beyond home, manifesto, docs (about, ai pages from reference are being removed, not ported)
- Backend or server-side rendering (static site only)
- Any framework migration (vanilla HTML/CSS/JS stays)
