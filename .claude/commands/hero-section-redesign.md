---
name: hero-section-redesign
description: Workflow command scaffold for hero-section-redesign in Harness.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /hero-section-redesign

Use this workflow when working on **hero-section-redesign** in `Harness`.

## Goal

Making significant changes to the homepage hero section, including layout, content, and CTA styling.

## Common Files

- `website/css/index.css`
- `website/index.html`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit hero layout and content in index.html.
- Update related CSS in index.css for new layout, typography, and button styles.
- Remove unused hero-related CSS classes.
- Test hero section for visual correctness and responsiveness.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.