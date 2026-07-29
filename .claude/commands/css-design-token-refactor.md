---
name: css-design-token-refactor
description: Workflow command scaffold for css-design-token-refactor in Harness.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /css-design-token-refactor

Use this workflow when working on **css-design-token-refactor** in `Harness`.

## Goal

Standardizing and refactoring CSS to use design tokens (CSS custom properties) instead of hardcoded values for colors, typography, and spacing.

## Common Files

- `website/css/global.css`
- `website/css/index.css`
- `website/css/nav.css`
- `website/css/style.css`
- `website/manifesto.html`
- `website/index.html`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Identify hardcoded CSS values in files like nav.css, global.css, index.css, style.css.
- Replace hardcoded colors, font sizes, and other properties with CSS custom properties (design tokens).
- Update HTML files (e.g., manifesto.html, index.html) if necessary to match new tokenized styles.
- Test for visual consistency and accessibility.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.