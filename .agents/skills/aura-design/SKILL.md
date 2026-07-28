# Aura Design System

Read **`BRAND_BRIEF.md`** first — that file is the philosophy and per-page contracts.
`DESIGN.md` is the token catalog (the only place hex / raw px-for-type literals may live).

## Core rules (BRAND_BRIEF.md is authoritative)

- No shadows on anything except optional product imagery — depth via tonal layering only
- Frosted glass nav: `backdrop-filter: blur(20px) saturate(180%)` — reserve glass for nav + cards on photo
- Only animate `transform` / `opacity` — never `transition: all`
- Body: 17px, 1.47 line-height, SF Pro Text
- Section padding: 80px desktop, 60px mobile
- Content max-width: 980px, hero max: 1200px, prose max: 680px

## Colors (use tokens, never raw values)

- `--color-ink` (#1d1d1f) — headlines, body text
- `--color-ink-secondary` (#333333) — secondary text
- `--color-ink-tertiary` (#7a7a7a) — captions, metadata
- `--color-canvas-white` (#fff) — primary background
- `--color-canvas-parchment` (#f5f5f7) — alternating sections
- `--color-canvas-dark` (#272729) — dark full-bleed tiles
- `--color-action-blue` (#0066cc) — single interactive accent (links, CTAs, eyebrows)

## Typography (five voices only)

Display, Hero, Tagline, Body, Caption. See `DESIGN.md` for the exact type-* tokens.

## Accessibility

- Skip link on every page
- Focus-visible rings on all interactive elements (already in global.css)
- `aria-hidden="true"` on decorative Lucide icons
- `prefers-reduced-motion` media query honored
- Touch targets ≥ 44px

## Reference

- `BRAND_BRIEF.md` — design philosophy + per-page section contracts (§9)
- `DESIGN.md` — token catalog
- `prompts/architect.py` — Architect system prompt
- `prompts/developer.py` — Developer system prompt
- `prompts/reviewer.py` — Reviewer system prompt (18-rule audit)
