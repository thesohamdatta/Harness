---
target: website homepage (index.html)
total_score: 24
max_score: 40
na_heuristics:
p0_count: 0
p1_count: 2
p2_count: 2
p3_count: 1
timestamp: 2026-07-27T19-17-28Z
slug: website-index-html
---

## Question

What is the current design quality baseline of the Aura website homepage, measured by Nielsen heuristics, Apple HIG compliance, cognitive load, and persona-based testing?

## Resolution

### Method

Critique performed against `website/index.html` using source file analysis, Impeccable detector scan, and design review criteria. No browser automation available; assessed via source code.

### Detector Findings

| File           | Issues                                                                 |
| -------------- | ---------------------------------------------------------------------- |
| index.html     | 21 font-size violations, 1 aphoristic-cadence copy                     |
| manifesto.html | 9 font-size violations                                                 |
| docs.html      | 33 font-size violations                                                |
| global.css     | 8 font-size violations, 2 radius violations                            |
| **Total**      | **~73 issues (all advisory, font-size/radius outside DESIGN.md ramp)** |

### Design Health Score

| #         | Heuristic                       | Score                  | Key Issue                                                                                                 |
| --------- | ------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------- |
| 1         | Visibility of System Status     | 3/4                    | Loading states absent, but static site has minimal async                                                  |
| 2         | Match System / Real World       | 2/4                    | "Less distraction. More done." reads as AI cadence; some copy generic                                     |
| 3         | User Control and Freedom        | 3/4                    | Nav is clear, back/forward works, but no undo in forms                                                    |
| 4         | Consistency and Standards       | 2/4                    | Typography scale differs between DESIGN.md and code; radius tokens inconsistent                           |
| 5         | Error Prevention                | 2/4                    | 404 page exists but no form validation patterns documented                                                |
| 6         | Recognition Rather Than Recall  | 3/4                    | Nav labels are clear; icon labels present                                                                 |
| 7         | Flexibility and Efficiency      | 2/4                    | No keyboard shortcuts; no power-user paths for docs                                                       |
| 8         | Aesthetic and Minimalist Design | 2/4                    | Glass effects overused; typography scale drift; shadow misuse (filter: drop-shadow instead of box-shadow) |
| 9         | Error Recovery                  | 2/4                    | 404 exists but no helpful guidance on it                                                                  |
| 10        | Help and Documentation          | 3/4                    | Docs page is thorough; no contextual inline help                                                          |
| **Total** |                                 | **24/40 (Acceptable)** |                                                                                                           |

### Design Specificity Verdict

The site is **partially specific** to Aura. The product photography, specs (0.5s latency, ~$50 BOM, 80g), and "third device" thesis are authentic. However:

- The Apple design language is well-executed in intent but has implementation drift (glass overuse, shadow wrong type, wrong type scale)
- Some copy reads as AI-generated cadence ("Not a computer. Not a phone. Something worn.")
- Category-interchangeable cards (icon + heading + text pattern repeated across sections)

### What's Working

1. Strong product photography and spec presentation (latency, BOM, weight numbers feel authentic)
2. Good semantic HTML structure with skip links and aria-current
3. Clean color palette that approximates the Apple look

### Priority Issues

1. **[P1] Type system drift**: 73+ font-size values outside DESIGN.md ramp. The site uses its own scale (48px, 64px, 80px, 36px, 32px, 19px, 15px, 13px, 11px) that doesn't match DESIGN.md's (56px, 40px, 34px, 28px, 21px, 17px, 14px, 12px, 10px). Either update DESIGN.md to reflect the actual ramp, or change code to match DESIGN.md. **Fix:** `$impeccable document` or `$impeccable typeset website/`

2. **[P1] Shadow misuse**: `.product-shadow` uses `filter: drop-shadow()` while DESIGN.md specifies `box-shadow: rgba(0, 0, 0, 0.22) 3px 5px 30px`. Also the values differ (Apple: 3px 5px 30px; current: 0 20px 40px + 0 6px 12px). **Fix:** `$impeccable polish website/`

3. **[P2] Radius drift**: Global CSS uses `border-radius: 10px` (scrollbar thumb) and `border-radius: 32px` (hero CTA container) which are outside DESIGN.md's `{rounded}` scale (5/8/11/18/9999px). **Fix:** `$impeccable polish website/`

4. **[P2] Glass overuse**: `.glass-card`, `.glass-card-dark`, `.glass-icon`, `.glass-btn`, `hero-pill`, `bento-pocket` all use backdrop-filter blur. Apple uses backdrop-filter only on `sub-nav-frosted` and `floating-sticky-bar`. **Fix:** `$impeccable polish website/` → `$impeccable quieter website/`

5. **[P3] Nav doesn't match DESIGN.md spec**: Current nav is a transparent/white overlay, not Apple's `{surface-black}` 44px global-nav with 52px sub-nav-frosted below. **Fix:** `$impeccable layout website/`

### Persona Red Flags

**Alex (Power User):** No keyboard shortcuts for docs navigation. One-at-a-time workflows where batch would be natural. No escape from long page scroll.

**Jordan (First-Timer):** "The third device" concept might not land in first 5 seconds. Hero image has low alt text. Icon-only mobile menu toggle (though it has aria-label).

**Casey (Mobile User):** No bottom-of-screen actions. Touch targets look adequate but responsive breakpoints only at 640px and 768px — no tablet optimization.

### Minor Observations

- `utils.css` loaded twice in `<head>` (lines 46-47)
- Footer has disabled links (Discord, Ethics, MIT License, Privacy) — these send mixed signals
- No `prefers-reduced-motion` intentional alternative (current global kill switch preserves state changes but should be verified)
- `--content-max: 980px` but DESIGN.md says 1440px for product grids
