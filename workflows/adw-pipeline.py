"""
ADW Pipeline Runner: Orchestrates Architect → Developer → Reviewer agents.

Usage:
    python workflows/adw-pipeline.py --all
    python workflows/adw-pipeline.py --page index
    python workflows/adw-pipeline.py --page manifesto
    python workflows/adw-pipeline.py --page docs
"""

import argparse
import asyncio
import os
import pathlib
import sys

from google.antigravity import Agent

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SPEC_DIR = ROOT / ".scratch" / "adw-pipeline" / "specs"
REVIEW_DIR = ROOT / ".scratch" / "adw-pipeline" / "reviews"
SPEC_DIR.mkdir(parents=True, exist_ok=True)
REVIEW_DIR.mkdir(parents=True, exist_ok=True)


SYSTEM_DIR = ROOT / "prompts"
PAGES = {
    "index": {
        "goal": "Build the homepage: a condensed 5-6 section marketing page that tells the Aura product story.",
        "spec_file": SPEC_DIR / "index.md",
        "review_file": REVIEW_DIR / "index.md",
    },
    "manifesto": {
        "goal": "Build the manifesto page: a long-form essay presenting the 'Third Device' philosophy.",
        "spec_file": SPEC_DIR / "manifesto.md",
        "review_file": REVIEW_DIR / "manifesto.md",
    },
    "docs": {
        "goal": "Build the docs page: comprehensive technical documentation covering specs, build guide, firmware, and companion app.",
        "spec_file": SPEC_DIR / "docs.md",
        "review_file": REVIEW_DIR / "docs.md",
    },
}


async def run_agent(config_module: str, prompt: str) -> str:
    """Run a single agent and return its full output."""
    import importlib

    mod = importlib.import_module(config_module)
    config = mod.create_config()
    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        chunks: list[str] = []
        async for token in response:
            print(token, end="", flush=True)
            chunks.append(token)
        print()
        return "".join(chunks)


async def architect(page: str, goal: str) -> str:
    """Run the Architect agent to produce a spec."""
    print(f"\n{'='*60}")
    print(f"  ARCHITECT → Planning: {page}")
    print(f"{'='*60}")
    prompt = (
        f"Produce a page spec for: {page}\n\n"
        f"Goal: {goal}\n\n"
        f"Reference site is at D:\\PROJECTS\\aura\\website\n"
        f"Design system is at D:\\PROJECTS\\aura\\website\\DESIGN.md\n"
        f"Existing new site is at D:\\PROJECTS\\Harness\\SDK\\website\n\n"
        f"Read the reference site's {page}.html and DESIGN.md, then produce a "
        f"structured spec document. Write the spec to {SPEC_DIR / f'{page}.md'}."
    )
    return await run_agent("prompts.architect", prompt)


async def developer(page: str) -> str:
    """Run the Developer agent to build from the spec."""
    spec_path = SPEC_DIR / f"{page}.md"
    if not spec_path.exists():
        print(f"  ⚠ No spec found for {page}, skipping.")
        return ""

    print(f"\n{'='*60}")
    print(f"  DEVELOPER → Building: {page}")
    print(f"{'='*60}")
    spec = spec_path.read_text(encoding="utf-8")
    prompt = (
        f"Build the page: {page}\n\n"
        f"## Spec\n{spec}\n\n"
        f"Write the HTML file to D:\\PROJECTS\\Harness\\SDK\\website\\{page}.html.\n"
        f"Copy any needed assets from D:\\PROJECTS\\aura\\website\\assets\\\n"
        f"Read existing css/global.css for design tokens.\n"
        f"Follow DESIGN.md rules strictly."
    )
    return await run_agent("prompts.developer", prompt)


async def reviewer(page: str) -> str:
    """Run the Reviewer agent to audit the built page."""
    print(f"\n{'='*60}")
    print(f"  REVIEWER → Auditing: {page}")
    print(f"{'='*60}")
    prompt = (
        f"Audit the page: {page}\n\n"
        f"Read D:\\PROJECTS\\Harness\\SDK\\website\\{page}.html and "
        f"all linked CSS files. Check against DESIGN.md rules.\n"
        f"Write the review report to {REVIEW_DIR / f'{page}.md'}."
    )
    return await run_agent("prompts.reviewer", prompt)


async def run_page(page: str) -> None:
    goal = PAGES[page]["goal"]
    print(f"\n{'#'*60}")
    print(f"  PIPELINE: {page}")
    print(f"{'#'*60}")

    # Stage 1: Architect
    spec = await architect(page, goal)
    if not spec:
        spec = f"See spec file: {PAGES[page]['spec_file']}"

    # Stage 2: Developer
    code = await developer(page)
    if not code:
        print(f"  ⚠ Developer produced no output for {page}")

    # Stage 3: Reviewer
    review = await reviewer(page)
    if not review:
        print(f"  ⚠ Reviewer produced no output for {page}")

    print(f"\n  ✓ Pipeline complete for: {page}")


async def run_all() -> None:
    for page in PAGES:
        await run_page(page)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ADW Pipeline Runner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all pages")
    group.add_argument("--page", choices=list(PAGES.keys()), help="Run one page")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    os.environ["GEMINI_API_KEY"] = api_key

    args = parse_args(argv)
    if args.all:
        asyncio.run(run_all())
    else:
        asyncio.run(run_page(args.page))


if __name__ == "__main__":
    main()
