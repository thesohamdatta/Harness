---
name: footer-component-redesign
description: Workflow command scaffold for footer-component-redesign in Harness.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /footer-component-redesign

Use this workflow when working on **footer-component-redesign** in `Harness`.

## Goal

Redesigning and refactoring the website footer for improved layout, accessibility, and consistency, often consolidating CSS and JS logic.

## Common Files

- `website/css/global.css`
- `website/css/index.css`
- `website/css/style.css`
- `website/js/footer.js`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Update footer layout and content in global.css and index.css.
- Remove or consolidate duplicate/legacy footer CSS from style.css and index.css.
- Rewrite or simplify footer.js for new structure and accessibility.
- Test footer on all relevant pages (index.html, etc.).

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.