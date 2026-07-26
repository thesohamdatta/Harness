"""
Prompt Engineer — structured prompt builder for the harness.

Encodes Anthropic's prompt engineering best practices (2026):
  - XML-tagged sections for unambiguous structure
  - Long context at top, query at bottom
  - Positive instructions over prohibitions
  - Role prompting per agent
  - Progressive disclosure via lazy-loaded context blocks
  - Minimal boilerplate — modern models are over-constrained by default
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import Callable


TAG = "<{name}>\n{content}\n</{name}>"


def tag(name: str, content: str) -> str:
    return TAG.format(name=name, content=content.strip())


@dataclass
class Prompt:
    role: str
    context: list[str] = field(default_factory=list)
    instructions: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)

    def build(self) -> str:
        blocks: list[str] = []

        if self.role:
            blocks.append(tag("role", self.role))

        if self.context:
            blocks.append(tag("context", "\n\n".join(self.context)))

        if self.references:
            blocks.append(tag("references", "\n\n".join(self.references)))

        if self.instructions:
            numbered = "\n".join(
                f"{i+1}. {inst}" for i, inst in enumerate(self.instructions)
            )
            blocks.append(tag("instructions", numbered))

        if self.outputs:
            blocks.append(tag("output", "\n".join(self.outputs)))

        return "\n\n".join(blocks)


def build_prompt(
    role: str,
    instructions: list[str],
    context: list[str] | None = None,
    outputs: list[str] | None = None,
    references: list[str] | None = None,
) -> str:
    return Prompt(
        role=role,
        context=context or [],
        instructions=instructions,
        outputs=outputs or [],
        references=references or [],
    ).build()
