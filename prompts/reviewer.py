"""ADW Reviewer — audits built pages against DESIGN.md compliance."""

import pathlib

from google.antigravity.connections.local import LocalAgentConfig
from google.antigravity.types import BuiltinTools, CapabilitiesConfig
from prompts.engineer import build_prompt

WEBSITE_DIR = pathlib.Path(r"D:\PROJECTS\Harness\SDK\website")
REFERENCE_DIR = pathlib.Path(r"D:\PROJECTS\aura\website")

ROLE = (
    "You are the **Reviewer** in an ADW pipeline. "
    "You audit built pages against DESIGN.md rules. You never write code."
)

CONTEXT = [
    f"Audit target: {WEBSITE_DIR}. Reference design: {REFERENCE_DIR / 'DESIGN.md'}",
]

INSTRUCTIONS = [
    "Read the page HTML and its linked CSS files.",
    "Check each of these rules. Report PASS or FAIL for each:",
    "  — No box-shadow on buttons, cards, text, or nav",
    "  — No transition: all — only transform/opacity transitions",
    "  — Frosted glass nav: backdrop-filter: blur(20px) saturate(180%)",
    "  — Body font-size 17px, headings use tight tracking",
    "  — Colors use --var tokens, not raw hex (except in token definitions)",
    "  — Skip link present, focus-visible rings on interactive elements",
    "  — Images have width/height + descriptive alt",
    "  — prefers-reduced-motion media query present",
    "  — Touch targets >=44px, touch-action: manipulation",
    "  — No inline styles — styling via CSS classes",
    "Output a markdown report with Pass/Fail sections and a verdict.",
]

OUTPUTS = [
    "Save the report to .scratch/adw-pipeline/reviews/<page>.md",
    "Verdict: PASS / FAIL / PASS WITH NOTES",
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
        workspaces=[str(WEBSITE_DIR), str(REFERENCE_DIR)],
        capabilities=capabilities,
    )
