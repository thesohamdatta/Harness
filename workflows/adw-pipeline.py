"""
ADW Pipeline Runner: Orchestrates Architect → Developer → Reviewer agents
with quality gates and auto-retry on review failure.

Usage:
    python workflows/adw-pipeline.py --all
    python workflows/adw-pipeline.py --page index
    python workflows/adw-pipeline.py --page manifesto
    python workflows/adw-pipeline.py --page docs
    python workflows/adw-pipeline.py --all --dry-run
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

WEBSITE_DIR = ROOT / "website"
REFERENCE_DIR = pathlib.Path(r"D:\PROJECTS\aura\website")
DESIGN_MD = REFERENCE_DIR / "DESIGN.md"

PAGES = {
    "index": {
        "goal": "Build the homepage: a condensed marketing page that tells the Aura product story.",
    },
    "manifesto": {
        "goal": "Build the manifesto page: a long-form essay presenting the 'Third Device' philosophy.",
    },
    "docs": {
        "goal": "Build the docs page: comprehensive technical documentation with sidebar navigation.",
    },
}


async def run_agent(config_module: str, prompt: str, label: str = "") -> str:
    import importlib

    mod = importlib.import_module(config_module)
    config = mod.create_config()
    prefix = f"[{label}] " if label else ""
    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        chunks: list[str] = []
        async for token in response:
            print(f"{prefix}{token}", end="", flush=True)
            chunks.append(token)
        print()
        return "".join(chunks)


async def architect(page: str, goal: str) -> str:
    spec_path = SPEC_DIR / f"{page}.md"
    print(f"\n{'='*60}")
    print(f"  ARCHITECT → Planning: {page}")
    print(f"{'='*60}")
    prompt = (
        f"Produce a page spec for: {page}\n\n"
        f"Goal: {goal}\n\n"
        f"Reference site: {REFERENCE_DIR}\n"
        f"Design system: {DESIGN_MD}\n"
        f"Target build: {WEBSITE_DIR}\n\n"
        f"Read the reference site's {page if page != 'index' else 'index'}.html and DESIGN.md, "
        f"then produce a structured spec. "
        f"Write the spec to {spec_path}."
    )
    return await run_agent("prompts.architect", prompt, label="ARCH")


async def developer(page: str) -> str:
    spec_path = SPEC_DIR / f"{page}.md"
    if not spec_path.exists():
        print(f"  \u26a0 No spec found for {page}, skipping.")
        return ""

    print(f"\n{'='*60}")
    print(f"  DEVELOPER → Building: {page}")
    print(f"{'='*60}")
    spec = spec_path.read_text(encoding="utf-8")
    prompt = (
        f"Build the page: {page}\n\n"
        f"## Spec\n{spec}\n\n"
        f"Write the HTML file to {WEBSITE_DIR / f'{page}.html'}.\n"
        f"Copy any needed assets from {REFERENCE_DIR / 'assets'}/\n"
        f"Read existing css/global.css for design tokens.\n"
        f"Follow DESIGN.md rules strictly.\n"
        f"Nav is static HTML — copy nav block from an existing page, update active link."
    )
    return await run_agent("prompts.developer", prompt, label="DEV")


async def reviewer(page: str) -> str:
    review_path = REVIEW_DIR / f"{page}.md"
    print(f"\n{'='*60}")
    print(f"  REVIEWER → Auditing: {page}")
    print(f"{'='*60}")
    prompt = (
        f"Audit the page: {page}\n\n"
        f"Read {WEBSITE_DIR / f'{page}.html'} and all linked CSS files. "
        f"Check against DESIGN.md rules at {DESIGN_MD}.\n"
        f"Write the review to {review_path}.\n"
        f"Verdict must be: PASS / FAIL / PASS WITH NOTES."
    )
    return await run_agent("prompts.reviewer", prompt, label="REV")


def check_review_verdict(page: str) -> str:
    review_path = REVIEW_DIR / f"{page}.md"
    if not review_path.exists():
        return "NO_REVIEW"
    text = review_path.read_text(encoding="utf-8").lower()
    if "pass" in text and "fail" not in text:
        return "PASS"
    if "fail" in text:
        return "FAIL"
    return "PASS_WITH_NOTES"


async def run_page(page: str) -> dict:
    result = {"page": page, "architect": "", "developer": "", "reviewer": "", "verdict": "", "iterations": 0}
    print(f"\n{'#'*60}")
    print(f"  PIPELINE: {page}")
    print(f"{'#'*60}")

    # Stage 1: Architect
    spec = await architect(page, PAGES[page]["goal"])
    if not spec:
        spec = f"See spec file: {SPEC_DIR / f'{page}.md'}"
    result["architect"] = "done"

    # Stage 2: Developer
    code = await developer(page)
    if not code:
        print(f"  \u26a0 Developer produced no output for {page}")
        result["verdict"] = "FAILED_DEV"
        return result
    result["developer"] = "done"

    # Stage 3: Reviewer with up to 2 retry iterations
    for attempt in range(3):
        review = await reviewer(page)
        result["reviewer"] = "done"
        result["iterations"] = attempt + 1

        verdict = check_review_verdict(page)
        result["verdict"] = verdict

        if verdict == "PASS":
            print(f"\n  \u2713 Page '{page}' passed review on attempt {attempt + 1}")
            break
        elif verdict == "FAIL" and attempt < 2:
            print(f"\n  \u26a0 Review FAILED for '{page}' (attempt {attempt + 1}/3). Rebuilding...")
            code = await developer(page)
            if not code:
                break
        else:
            break

    print(f"\n  \u2713 Pipeline complete for: {page} (verdict: {result['verdict']})")
    return result


async def run_all() -> list[dict]:
    results = []
    for page in PAGES:
        r = await run_page(page)
        results.append(r)
    return results


def print_summary(results: list[dict]) -> None:
    print(f"\n{'='*60}")
    print(f"  PIPELINE SUMMARY")
    print(f"{'='*60}")
    for r in results:
        verdict = r["verdict"]
        icon = "\u2713" if verdict == "PASS" else "\u2717" if verdict == "FAIL" else "\u26a0"
        print(f"  {icon} {r['page']}: {verdict} ({r['iterations']} review iteration(s))")
    all_pass = all(r.get("verdict") == "PASS" for r in results)
    print(f"\n  Overall: {'ALL PASS' if all_pass else 'SOME ISSUES'}")
    print(f"{'='*60}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ADW Pipeline Runner")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--all", action="store_true", help="Run all pages")
    group.add_argument("--page", choices=list(PAGES.keys()), help="Run one page")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without running")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    os.environ["GEMINI_API_KEY"] = api_key

    args = parse_args(argv)

    if args.dry_run:
        print(f"Pipeline plan:")
        pages = PAGES if args.all else ([args.page] if args.page else ["(none)"])
        for p in pages:
            print(f"  - {p}: Architect → Developer → Reviewer (up to 3 review cycles)")
        print(f"  Output: specs in {SPEC_DIR}, reviews in {REVIEW_DIR}")
        return

    pages_to_run = list(PAGES.keys()) if args.all or not args.page else [args.page]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if len(pages_to_run) == 1:
            r = loop.run_until_complete(run_page(pages_to_run[0]))
        else:
            results = loop.run_until_complete(run_all())
            print_summary(results)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
