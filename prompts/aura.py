"""
Aura website dev harness config.

Usage:
    python -m prompts.aura "add an FAQ section to index.html"
    python agent_harness.py --aura "audit the CSS for contrast issues"
"""

import os
import pathlib
import sys

from google.antigravity.connections.local import LocalAgentConfig
from google.antigravity.types import BuiltinTools, CapabilitiesConfig
from prompts.engineer import build_prompt

WEBSITE_DIR = pathlib.Path(r"D:\PROJECTS\Harness\SDK\website")
REFERENCE_DIR = pathlib.Path(r"D:\PROJECTS\aura\website")

ROLE = "You are a web dev assistant for the Aura project. The harness SDK runtime is at D:\\PROJECTS\\Harness\\SDK."

CONTEXT = [
    "Aura is an open-source, screenless, voice-first AI pendant. This repo builds a static GitHub Pages website for it.",
    f"Reference site (content + assets): {REFERENCE_DIR}",
    f"Build directory: {WEBSITE_DIR}",
    "Stack: Vanilla HTML/CSS/JS, Tailwind CDN, Lucide icons from unpkg, SF Pro from local assets.",
    "Design tokens in css/global.css — use --var tokens exclusively.",
    "Shared nav in js/nav.js mounted into #nav-mount. Shared footer in js/footer.js into #footer-mount.",
]

INSTRUCTIONS = [
    "Animate transform/opacity only — never transition: all.",
    "Use design tokens for all colors and typography.",
    "Include skip-link, focus-visible rings, aria-hidden on decorative icons.",
    "Set explicit width/height on images, loading='lazy' below fold.",
    "Honor prefers-reduced-motion.",
]

SYSTEM_INSTRUCTIONS = build_prompt(
    role=ROLE,
    context=CONTEXT,
    instructions=INSTRUCTIONS,
    references=[
        f"Design system: {REFERENCE_DIR / 'DESIGN.md'}",
        f"Reference site (read for copy + patterns): {REFERENCE_DIR}",
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
        workspaces=[str(WEBSITE_DIR), str(REFERENCE_DIR)],
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
