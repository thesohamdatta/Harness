# Aura Design System

Design rules for the Aura website. Source of truth is `DESIGN.md` in the reference site.

## Core rules
- No shadows on anything — depth via tonal layering only
- Frosted glass nav: `backdrop-filter: blur(20px) saturate(180%)`
- Only animate `transform`/`opacity` — never `transition: all`
- Body: 17px, 1.47 line-height, SF Pro Text
- Section padding: 80px desktop, 60px mobile
- Content max-width: 980px, hero max: 1200px

## Colors (use tokens, not raw values)
- `--color-ink` (#1d1d1f) — headlines, body text
- `--color-ink-secondary` (#6e6e73) — captions, metadata
- `--color-canvas-white` (#fff) — primary background
- `--color-canvas-parchment` (#f5f5f7) — alternating sections
- `--color-action-blue` (#0066cc) — links, CTAs

## Accessibility
- Skip link on every page
- Focus-visible rings on all interactive elements
- aria-hidden="true" on decorative icons
- prefers-reduced-motion media query
