"""ADW Developer — builds pages from Architect specs."""

import pathlib

from google.antigravity.connections.local import LocalAgentConfig
from google.antigravity.types import BuiltinTools, CapabilitiesConfig
from prompts.engineer import build_prompt

WEBSITE_DIR = pathlib.Path(r"D:\PROJECTS\Harness\SDK\website")
REFERENCE_DIR = pathlib.Path(r"D:\PROJECTS\aura\website")
HARNESS_DIR = pathlib.Path(r"D:\PROJECTS\Harness\SDK")

ROLE = "You are the **Developer** in an ADW pipeline. You translate page specs into working HTML/CSS/JS files."

CONTEXT = [
    f"Target directory: {WEBSITE_DIR}",
    f"Reference site (copy assets from): {REFERENCE_DIR}",
    "Stack: Vanilla HTML/CSS/JS, Tailwind CDN, Lucide icons from unpkg, SF Pro fonts from local assets.",
    "Design tokens in css/global.css — use --var tokens, never raw hex.",
    "Shared nav in js/nav.js mounted into #nav-mount. Shared footer in js/footer.js into #footer-mount.",
]

INSTRUCTIONS = [
    "Read the spec from .scratch/adw-pipeline/specs/<page>.md first.",
    "Write the HTML file to website/<page>.html.",
    "Animate transform/opacity only — never transition: all.",
    "Use design tokens from global.css for all colors and typography.",
    "Copy needed assets from reference site if they don't exist in website/assets/.",
    "Include skip-link, focus-visible rings, aria-hidden on decorative icons, prefers-reduced-motion.",
    "Set explicit width/height on images, loading='lazy' below fold.",
]

OUTPUTS = [
    "HTML file at website/<page>.html, with existing css/global.css + js/ for shared components.",
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
        workspaces=[str(WEBSITE_DIR), str(REFERENCE_DIR), str(HARNESS_DIR)],
        capabilities=capabilities,
    )
