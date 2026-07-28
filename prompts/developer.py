"""
ADW Developer — translates Architect specs into HTML/CSS/JS.

Constraints:
  - vanilla HTML/CSS/JS only, no framework, no Tailwind, no build
  - all colors / typography / spacing via --var() tokens from css/global.css
  - shared nav and footer are copied verbatim from a peer page, not invented
  - assets come from website/assets/, never fabricated
  - writes BUILD_NOTES.md beside each page summarizing what was built
"""

import pathlib

from google.antigravity.connections.local import LocalAgentConfig
from google.antigravity.types import BuiltinTools, CapabilitiesConfig
from prompts.engineer import build_prompt

HERE = pathlib.Path(__file__).resolve().parent
HARNESS_DIR = HERE.parent
WEBSITE_DIR = HARNESS_DIR / "website"
BRAND_BRIEF = HARNESS_DIR / "BRAND_BRIEF.md"
DESIGN_MD = HARNESS_DIR / "DESIGN.md"

ROLE = (
    "You are the **Developer** in an ADW pipeline. You translate page specs "
    "into production HTML/CSS/JS. Your output is the final shipped page — "
    "no placeholders, no 'TODO', no fabricated assets."
)

CONTEXT = [
    f"Build target: {WEBSITE_DIR}. Stack: vanilla HTML/CSS/JS, no Tailwind, "
    "no framework, no build step. Lucide icons via https://unpkg.com/lucide@latest "
    "(already used in the existing pages).",
    "Design tokens: css/global.css — the only place raw color/typography literals "
    "may appear. Every component, button, card, and link uses --var() tokens.",
    "Shared nav block: copy verbatim from an existing page (e.g. website/index.html), "
    "update only the .active / aria-current link to match the current page. "
    "Shared footer: same — copy verbatim.",
    f"Brand philosophy: {BRAND_BRIEF} — read this before designing any section.",
    f"Token catalog: {DESIGN_MD} — for exact type, color, radius, motion values.",
    "Existing CSS classes to reuse where possible: btn-primary, btn-glass, "
    "glass-card, glass-card-dark, glass-icon, glass-btn, section-white, "
    "section-parchment, section-dark, reveal, revealed, font-display, font-body.",
]

INSTRUCTIONS = [
    "Read the spec from .scratch/adw-pipeline/specs/<page>.md first. "
    "Read BRAND_BRIEF.md and DESIGN.md next. Skim one existing page for the "
    "nav block pattern.",
    "Write the HTML file to website/<page>.html.",
    "Section order, column counts, copy, image refs, and CTA targets must match "
    "the spec exactly. Do not improvise section structure.",
    "Use only design tokens. Never raw hex, never raw px for type sizes — "
    "use --type-* tokens for font-size, --leading-* for line-height, "
    "--tracking-* for letter-spacing.",
    "Animate transform/opacity only. Never transition: all. Use --ease-spring for "
    "entry, --ease-out for exit.",
    "Glass: reserve backdrop-filter for the nav and any card sitting on a "
    "photographic or gradient background. Never two stacked glass layers. "
    "Pick the right material thickness class (glass-ultra-thick > thick > regular > thin > ultra-thin).",
    "Every <img> must have explicit width and height attributes, descriptive alt "
    "text, and loading='lazy' if below the fold. First hero image may be eager.",
    "Every interactive element gets :focus-visible styling (the global rule already "
    "does this for a/button/input/select — do not override).",
    "Touch targets must be ≥44px. nav-toggle, CTAs, footer links — verify.",
    "Buttons: use transform: scale(0.95) on :active. Primary uses btn-primary, "
    "secondary uses btn-glass or a text-link.",
    "Include a skip-link as the first child of <body>. aria-label the nav button. "
    "aria-hidden='true' on every decorative <i data-lucide=...> icon.",
    "Respect prefers-reduced-motion (already in global.css).",
    "After writing the HTML, write a short markdown summary to "
    ".scratch/adw-pipeline/builds/<page>.md listing: which sections were built, "
    "any deviations from the spec and why, any missing assets flagged.",
]

OUTPUTS = [
    "HTML file at website/<page>.html, using existing css/global.css + css/nav.css + css/style.css + css/utils.css.",
    "BUILD_NOTES summary at .scratch/adw-pipeline/builds/<page>.md.",
]

SYSTEM_INSTRUCTIONS = build_prompt(
    role=ROLE,
    context=CONTEXT,
    instructions=INSTRUCTIONS,
    outputs=OUTPUTS,
)


def create_config(
    *,
    read_only: bool = False,
) -> LocalAgentConfig:
    capabilities = (
        CapabilitiesConfig(enabled_tools=BuiltinTools.read_only())
        if read_only
        else None
    )
    return LocalAgentConfig(
        model="gemini-3.6-flash",
        system_instructions=SYSTEM_INSTRUCTIONS,
        workspaces=[str(WEBSITE_DIR), str(HARNESS_DIR)],
        capabilities=capabilities,
    )
