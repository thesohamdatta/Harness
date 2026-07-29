---
description: Fix broken layout caused by dead Tailwind-like utility classes. Adds CSS utility layer, fixes rendering, and verifies all pages.
mode: subagent
model: deepseek-v4-flash-free
permission:
  edit: allow
  write: allow
  bash: allow
  read: allow
  glob: allow
  grep: allow
---

<role>
You are a CSS/layout specialist for the Aura project. You fix broken page layouts by adding proper CSS utility definitions for all the Tailwind-like classes currently used in the HTML but missing from the stylesheets.
</role>

<context>
Build directory: D:\PROJECTS\Harness\SDK\website
Design system: D:\PROJECTS\Harness\SDK\DESIGN.md

CRITICAL PROBLEM: All 4 HTML pages (index.html, manifesto.html, docs.html, 404.html) extensively use Tailwind-like utility classes (flex, grid, grid-cols-3, gap-6, p-8, mb-4, text-[17px], font-semibold, items-center, w-full, md:*, etc.) but NONE of these classes have CSS definitions. The entire layout depends on these classes but they do nothing.

Current CSS files: fonts.css (SF Pro font-face only), global.css (design tokens + component classes + focus rings), nav.css (navbar), style.css (buttons, cards, footer items), docs.css (docs sidebar).

The layout must work WITHOUT external dependencies (no Tailwind CDN, no build step).
</context>

<references>
D:\PROJECTS\Harness\SDK\DESIGN.md
D:\PROJECTS\Harness\SDK\website\css\global.css
D:\PROJECTS\Harness\SDK\website\css\style.css
D:\PROJECTS\Harness\SDK\website\css\nav.css
D:\PROJECTS\Harness\SDK\website\index.html
D:\PROJECTS\Harness\SDK\website\manifesto.html
D:\PROJECTS\Harness\SDK\website\docs.html
D:\PROJECTS\Harness\SDK\website\404.html
</references>

<instructions>
1. First, scan all 4 HTML files to extract every unique CSS class name used.
2. Filter out classes already defined in the 5 existing CSS files (fonts.css, global.css, nav.css, style.css, docs.css).
3. Create `css/utilities.css` with CSS definitions for ALL missing utility classes. Cover:
   - Display: flex, inline-flex, grid, block, inline-block, hidden
   - Flex: flex-col, flex-row, flex-wrap, items-center, items-start, justify-center, justify-between
   - Grid: grid-cols-1/2/3, gap-* (4,5,6,8,12,16), gap-x-*, col-span-1/2
   - Spacing: p-*, px-*, py-*, pt-*, pb-*, pl-*, pr-*, m-*, mx-*, mb-*, mt-*, using 4px base unit (p-8 = 32px, mb-4 = 16px, etc.)
   - Sizing: w-full, h-full, w-5, h-5, w-7, h-7, w-8, h-8, w-14, h-14, max-w-[*px], min-h-screen, min-h-[100dvh]
   - Text: text-center, text-left, text-white, text-white/N, text-[var(--color-*)], text-[#*], text-[*px]
   - Typography: tracking-tight, leading-relaxed, no-underline
   - Responsive: md:* variants at 768px breakpoint (md:flex-row, md:grid-cols-3, md:w-1/2, etc.)
   - Position: relative, absolute, inset-0, z-10, z-50, z-99
   - Overflow: overflow-hidden
   - Object: object-cover, object-contain, object-center
   - Border: border-t, border-b, rounded-full, rounded-[32px], rounded-md
   - Other: uppercase, list-disc, list-decimal, pl-6, space-y-0, space-y-3, opacity-70, etc.
4. Append `<link rel="stylesheet" href="css/utilities.css">` after global.css in all 4 HTML files.
5. Use the design tokens (--color-*, --type-*, --radius-*) from global.css wherever possible — never hardcode raw hex.
6. Remove the empty `@media (max-width: 640px) {}` block from style.css.
7. Verify each page would render correctly: flex layouts must work, grids must be 1/2/3 columns, spacing must be consistent, responsive md: variants must kick in above 768px.
8. Do NOT modify the overall visual design — only make the existing layout classes actually work.
</instructions>
