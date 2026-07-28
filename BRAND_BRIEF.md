# Aura Brand Brief — Apple HIG Translation

> **Read this file before DESIGN.md.** DESIGN.md is the _token catalog_; this file is the _design philosophy_. Both must be honored.

Aura's marketing site is modeled after apple.com. Every section must feel like it could ship on apple.com and have only the wordmark changed. If a section would look at home on a Bootstrap marketing template, it does not belong here.

## 1. Hierarchy of surface

Apple's web pages follow a strict rhythm:

1. **Full-bleed photographic hero** — single product image, generous dark space, one headline, one tagline, no buttons competing with the photo.
2. **Full-bleed dark tile** — large headline, white text, optional 3-up glass sub-card row.
3. **Full-bleed light tile** — headline + supporting copy + photography, alternating.
4. **Section that breathes** — single product attribute on a parchment or pearl background.
5. **Closing CTA band** — single action, centered, no sidebar.

Every page follows this rhythm. Section padding is 80px desktop, 60px mobile. **Sections are separated only by background color, never by horizontal rules or shadows.**

## 2. The five typographic voices

Use exactly five sizes in any given page. No more.

| Voice   | Token                                         | Used for                                  |
| ------- | --------------------------------------------- | ----------------------------------------- |
| Display | `--type-display-2xl` / `display-xl` (48–64px) | Section headlines                         |
| Hero    | `--type-hero-display` (56–80px)               | Page hero only, one per page              |
| Tagline | `--type-tagline` (21px, weight 600)           | Sub-headlines, eyebrow on dark tiles      |
| Body    | `--type-body` (17px)                          | All paragraph text, never smaller in body |
| Caption | `--type-caption` (14px)                       | Footer, metadata, fine print              |

Eyebrows (`--type-eyebrow`, 13px, weight 600, Action Blue on light / 60% white on dark) sit _above_ the display headline they describe. Never inline. Never colored anything else.

## 3. Color discipline

- **One accent color.** Action Blue `#0066cc` is the only color that may draw attention. Eyebrows, links, primary CTAs, focus rings.
- **No greys other than the token palette.** Never `#888`, `#aaa`, `#999`. Use `--color-ink-muted-53` (`#86868b`) or `--color-ink-tertiary` (`#7a7a7a`).
- **No hex literals in component CSS.** Always `--var()`. Hex literals exist _only_ in `global.css` token definitions.
- **No brand accents.** No purple, no green, no orange. The dark tile is `--color-canvas-dark` (`#272729`), not pure black; the parchment tile is `--color-canvas-parchment` (`#f5f5f7`).

## 4. Glass — a hierarchy, not a prop

Backdrop-filter is a **structural** effect on apple.com, used to indicate _layering above scrollable content_. Reserve it for:

- The fixed navigation bar (always).
- Modal sheets and pull-up panels (if any).
- Card-like surfaces that sit _above_ a photographic or gradient background.

Do **not** put glass on:

- Capability cards on a flat white background (use plain `--color-canvas-parchment` instead).
- Buttons (solid pill, never glass).
- The 404 page or any low-information surface.

Material hierarchy (always pick the right one):

| Class                             | When                                      |
| --------------------------------- | ----------------------------------------- |
| `glass-ultra-thick`               | Sheets, primary modal panels              |
| `glass-thick`                     | The nav after scroll                      |
| `glass-regular`                   | The nav at top of page                    |
| `glass-thin` / `glass-ultra-thin` | Over high-motion photographic backgrounds |

Never two glass layers stacked. Never glass on glass.

## 5. Motion as restraint

- Animate **transform** and **opacity only.** No `transition: all`.
- Spring easing `--ease-spring` for entry, `--ease-out` for exit.
- Hover states: subtle (opacity 0.85 on primary, color shift on text).
- Active states: `transform: scale(0.95)` on all tappable elements.
- Respect `prefers-reduced-motion`.
- Scroll-reveal is allowed _once per section_, never on every paragraph.

## 6. Photography is the product

Where apple.com uses photography, Aura uses photography too — the pendant on a collar, the components exploded, the BOM laid out. **Never** substitute illustrations, abstract gradients, or 3D renders where a product photo is the right answer.

Hero photo carries 60–80% of the visual weight. Text on the hero should feel _added_, not _primary_.

## 7. The voice

- **Confident, not promotional.** "Listen, see, remember." not "Listen, see, remember — the most amazing AI ever!"
- **Short sentences.** The homepage hero copy is ≤ 14 words. Section headlines are ≤ 6 words.
- **No exclamation marks.** None.
- **No emoji.** None.
- **No superlatives.** No "best", "revolutionary", "cutting-edge".

## 8. What we are explicitly not

- Not Material Design. No elevation shadows on cards.
- Not Tailwind defaults. No `bg-blue-500`. Every color is a token.
- Not a dashboard. No metric tiles, no charts, no data viz unless documenting specs.
- Not a SaaS landing page. No "trusted by 10,000 customers", no logos bar.
- Not a tech-bro blog. No gradients-on-text, no neon accents, no glass-everything.

## 9. Per-page contracts

**`index.html`** — five sections, in this order:

1. Hero (photographic, dark, one CTA "Build yours" → docs.html#hardware)
2. Capabilities (3-up glass-card row on white — exception to "no glass on white" because each card sits above a subtle radial gradient backdrop, see hero-pill pattern)
3. The Third Device (full-bleed dark tile with 3 small glass sub-cards)
4. Specifications (parchment tile, exploded-view product image + 3 metric columns)
5. Build CTA (light tile, side-by-side product photo + two buttons)

**`manifesto.html`** — single-column essay, prose max-width 680px, hero-less, no decorative photography. Headline "We need a third device." Three sub-sections: _The problem_, _Why Aura_, _Closing_.

**`docs.html`** — sidebar (left, 240px, sticky) + content (right). Sidebar lists: Hardware, Firmware, Backend, Companion App, FAQ. Content is long-form with `h2` per section, code blocks in mono font, copy-to-clipboard buttons on each code block.

**`404.html`** — single centered column, big "404" display, one button back to index. No nav. No footer.

## 10. The contract the harness enforces

Every ADW agent must satisfy these in order. A section that violates one violates all.

1. Hierarchy of surface — five sections in the rhythm above.
2. Five typographic voices — no others.
3. One accent color — Action Blue only.
4. Glass reserved for nav + on-photo contexts.
5. Motion restricted to transform/opacity.
6. Photography preferred over illustration.
7. Voice rules — short, no exclamations, no superlatives.
8. Per-page section contract — exact section list and order.

If a spec, build, or review violates any of these, mark it BLOCKER.
