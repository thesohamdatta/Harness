"""
Aura website dev harness config.

Single-shot agent for general Aura web-dev questions. The ADW pipeline
(workflows/adw-pipeline.py) is the right tool for build tasks; this is
for one-off asks like "add an FAQ section" or "audit the CSS for contrast issues".
"""

import os
import pathlib
import sys

from google.antigravity.connections.local import LocalAgentConfig
from google.antigravity.types import BuiltinTools, CapabilitiesConfig
from prompts.engineer import build_prompt

HERE = pathlib.Path(__file__).resolve().parent
HARNESS_DIR = HERE.parent
WEBSITE_DIR = HARNESS_DIR / "website"
BRAND_BRIEF = HARNESS_DIR / "BRAND_BRIEF.md"
DESIGN_MD = HARNESS_DIR / "DESIGN.md"

ROLE = (
    "You are a web dev assistant for the Aura project. "
    "Aura is an open-source, screenless, voice-first AI pendant (~$50 BOM, MIT). "
    "You work on the Aura marketing site, modeled after apple.com."
)

CONTEXT = [
    "Stack: Vanilla HTML/CSS/JS. No Tailwind, no framework, no build step. "
    "Lucide icons from https://unpkg.com/lucide@latest. SF Pro fonts served "
    "from website/assets/fonts/sf-pro/.",
    f"Build directory: {WEBSITE_DIR}. Shared nav and footer are inline HTML "
    "copied across pages — never JS-rendered.",
    f"Brand philosophy (read first): {BRAND_BRIEF}",
    f"Design tokens (the only place hex/px-for-type literals may live): {DESIGN_MD}",
    "All components live in css/global.css, css/nav.css, css/style.css, css/utils.css. "
    "Add new classes there, never inline styles.",
]

INSTRUCTIONS = [
    "Animate transform/opacity only — never transition: all.",
    "Use design tokens (--var()) for all colors, typography, radius, motion. "
    "Never raw hex in component code; never raw px for font-size.",
    "Glass: reserve backdrop-filter for the nav and for cards sitting above "
    "photographic/gradient backgrounds. Never stack glass on glass.",
    "Include skip-link, focus-visible rings, aria-hidden on decorative icons.",
    "Set explicit width and height on every image, loading='lazy' below the fold.",
    "Honor prefers-reduced-motion.",
    "Buttons use transform: scale(0.95) on :active.",
    "No shadows on cards, buttons, or text — only on product imagery if absolutely needed.",
    "Voice: confident, short, no exclamation marks, no superlatives, no emoji.",
]

SYSTEM_INSTRUCTIONS = build_prompt(
    role=ROLE,
    context=CONTEXT,
    instructions=INSTRUCTIONS,
    references=[
        f"Brand brief: {BRAND_BRIEF}",
        f"Design tokens: {DESIGN_MD}",
    ],
)


def create_config(
    *,
    model: str = "gemini-3.6-flash",
    read_only: bool = False,
) -> LocalAgentConfig:
    capabilities = (
        CapabilitiesConfig(enabled_tools=BuiltinTools.read_only())
        if read_only
        else None
    )
    return LocalAgentConfig(
        model=model,
        system_instructions=SYSTEM_INSTRUCTIONS,
        workspaces=[str(WEBSITE_DIR), str(HARNESS_DIR)],
        capabilities=capabilities,
    )


if __name__ == "__main__":
    from agent_harness import run

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    config = create_config()

    import asyncio
    asyncio.run(run(prompt.strip(), config))
