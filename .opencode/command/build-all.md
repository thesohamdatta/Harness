---
description: Run full ADW pipeline for all pages. Usage: /build-all
agent: builder
model: deepseek-v4-flash-free
---

<role>You are the ADW pipeline runner. Build all website pages: index, manifesto, docs.</role>

<instructions>
1. Read DESIGN.md at D:\PROJECTS\aura\website\DESIGN.md
2. Read existing CSS at D:\PROJECTS\Harness\SDK\website\css\global.css, nav.css, style.css
3. For each page (index, manifesto, docs):
   a. Read the reference from D:\PROJECTS\aura\website\
   b. Plan and build the page at D:\PROJECTS\Harness\SDK\website\
   c. Copy needed assets
   d. Audit against DESIGN.md
   e. Fix issues
4. Verify all pages load correctly with the shared navbar and footer
5. Generate a brief summary of what was built and any known issues

Rules:

- Static navbar identical across all pages
- Glassmorphism on feature cards
- --var tokens only
- Natural copy
- Full a11y compliance
</instructions>
