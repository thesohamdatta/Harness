"""ADW Architect — produces page specs from goals + design system."""

import os
import pathlib
import sys

from google.antigravity.connections.local import LocalAgentConfig
from prompts.engineer import build_prompt

WEBSITE_DIR = pathlib.Path(r"D:\PROJECTS\Harness\SDK\website")
REFERENCE_DIR = pathlib.Path(r"D:\PROJECTS\aura\website")
HARNESS_DIR = pathlib.Path(r"D:\PROJECTS\Harness\SDK")
DESIGN_MD = REFERENCE_DIR / "DESIGN.md"

ROLE = (
    "You are the **Architect** in an ADW (Architect-Developer-Reviewer) pipeline. "
    "You produce structured page specs — you never write code."
)

CONTEXT = [
    "The Aura website is a 3-page static marketing site: index (homepage, ~6 sections), "
    "manifesto (philosophy essay), docs (build manual). Reference site is at "
    f"{REFERENCE_DIR}. Target build directory is {WEBSITE_DIR}.",
    f"Design system: {DESIGN_MD}. Every design decision must reference it.",
]

INSTRUCTIONS = [
    "Read the relevant page from the reference site and DESIGN.md.",
    "Produce a structured spec for each page in markdown.",
    "Keep specs focused: purpose, sections, components, content sources, design constraints.",
]

OUTPUTS = [
    "Save the spec to .scratch/adw-pipeline/specs/<page>.md",
    "Format: markdown with sections for Purpose, Sections, Components, Content, Constraints.",
]

SYSTEM_INSTRUCTIONS = build_prompt(
    role=ROLE,
    context=CONTEXT,
    instructions=INSTRUCTIONS,
    outputs=OUTPUTS,
)


def create_config() -> LocalAgentConfig:
    return LocalAgentConfig(
        model="gemini-3.6-flash",
        system_instructions=SYSTEM_INSTRUCTIONS,
        workspaces=[str(WEBSITE_DIR), str(REFERENCE_DIR), str(HARNESS_DIR)],
    )
