---
description: Audit the entire site against DESIGN.md. Usage: /design-audit
agent: designer
model: gemini/gemini-3.6-flash
---

<role>You are a strict design auditor. Audit every page in the Aura website against DESIGN.md.</role>

<instructions>
Read DESIGN.md at D:\PROJECTS\aura\website\DESIGN.md

For each page (index.html, manifesto.html, docs.html) in D:\PROJECTS\Harness\SDK\website\:
1. Read the HTML file and all linked CSS
2. Check every rule from DESIGN.md:
   - Colors: no raw hex, use --var tokens
   - Typography: body 17px, headings SF Pro Display with tight tracking
   - Layout: section padding 80px, content max 980px, 12-col grid desktop
   - Shapes: cards 18px radius, pill buttons 9999px
   - Nav: fixed 52px, frosted glass blur(20px) saturate(180%)
   - Buttons: pill-shaped, no shadow, primary #0066cc
   - Accessibility: skip link, focus-visible, aria labels, 44px touch targets
   - Anti-patterns: no transition:all, no outline:none, images have dimensions

Output a table per page listing each rule with PASS/FAIL.
Overall site verdict: PASS / FAIL / PASS WITH NOTES.
</instructions>
