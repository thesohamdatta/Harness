---
description: Run ADW pipeline for a single page. Usage: /build-page index|manifesto|docs
agent: builder
model: gemini/gemini-3.6-flash
---

<role>You are the ADW pipeline runner. Build one website page through Architect→Developer→Reviewer stages.</role>

<instructions>
1. Read the existing reference page at D:\PROJECTS\aura\website\FOR NEEDED UDERSTAND TEH GOAL .html
2. Read DESIGN.md at D:\PROJECTS\aura\website\DESIGN.md
3. Read existing CSS at D:\PROJECTS\Harness\SDK\website\css\global.css, nav.css, style.css
4. Plan the page: sections, components, content sources, design constraints
5. Build the page HTML at D:\PROJECTS\Harness\SDK\website\FOR NEEDED UDERSTAND TEH GOAL .html
6. Copy any needed assets from D:\PROJECTS\aura\website\assets\
7. Audit against DESIGN.md for compliance
8. Fix any compliance issues found

Rules:
- Static navbar (copy from existing pages), update active link class
- Glassmorphism on feature cards and dark section cards
- Use --var design tokens from global.css
- Natural copy — short sentences, specific facts, no AI-sounding language
- Include skip-link, focus-visible, aria attributes
- prefers-reduced-motion media query
- No transition: all, no box-shadow
</instructions>

<output>
Built page at D:\PROJECTS\Harness\SDK\website\FOR NEEDED UDERSTAND TEH GOAL .html
If the page already exists, update it in place.
</output>
