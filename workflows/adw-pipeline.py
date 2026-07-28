"""
ADW Pipeline Runner: Architect → Developer → Reviewer with quality gates.

Each page runs the loop:
    Architect → Developer → Reviewer
                            │
                            ├─ PASS                → done
                            ├─ PASS WITH NOTES     → done (nits logged)
                            └─ FAIL                → re-Architect with failure context
                                                  → re-Develop
                                                  → re-Review
                                                  (up to 3 total cycles)

Outputs are snapshotted under .scratch/adw-pipeline/runs/<page>/<iter>/ so the
full conversation history is auditable.

Usage:
    python workflows/adw-pipeline.py --all
    python workflows/adw-pipeline.py --page index
    python workflows/adw-pipeline.py --all --dry-run
"""

import argparse
import asyncio
import importlib
import json
import os
import pathlib
import sys
import time

from google.antigravity import Agent

HERE = pathlib.Path(__file__).resolve().parent
HARNESS_DIR = HERE.parent

SPEC_DIR = HARNESS_DIR / ".scratch" / "adw-pipeline" / "specs"
REVIEW_DIR = HARNESS_DIR / ".scratch" / "adw-pipeline" / "reviews"
BUILD_DIR = HARNESS_DIR / ".scratch" / "adw-pipeline" / "builds"
RUNS_DIR = HARNESS_DIR / ".scratch" / "adw-pipeline" / "runs"
WEBSITE_DIR = HARNESS_DIR / "website"
BRAND_BRIEF = HARNESS_DIR / "BRAND_BRIEF.md"
DESIGN_MD = HARNESS_DIR / "DESIGN.md"

for d in (SPEC_DIR, REVIEW_DIR, BUILD_DIR, RUNS_DIR):
    d.mkdir(parents=True, exist_ok=True)

MAX_CYCLES = 3

PAGES = {
    "index": {
        "goal": (
            "Build the homepage: a 5-section marketing page that introduces Aura, "
            "lists capabilities, presents the 'third device' philosophy, gives "
            "specs, and closes with a build CTA. See BRAND_BRIEF §9 for the "
            "exact section contract."
        ),
    },
    "manifesto": {
        "goal": (
            "Build the manifesto page: a long-form essay presenting the 'Third "
            "Device' philosophy. Single-column prose, 680px max-width, no "
            "decorative photography. See BRAND_BRIEF §9."
        ),
    },
    "docs": {
        "goal": (
            "Build the docs page: comprehensive technical documentation with a "
            "240px sticky left sidebar and long-form content on the right. "
            "Sections: Hardware, Firmware, Backend, Companion App, FAQ. See "
            "BRAND_BRIEF §9."
        ),
    },
}


async def run_agent(config_module: str, prompt: str, label: str = "") -> str:
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


def write_snapshot(run_dir: pathlib.Path, stage: str, prompt: str, response: str) -> None:
    """Save (prompt, response) for a single stage to disk."""
    stage_dir = run_dir / stage
    stage_dir.mkdir(parents=True, exist_ok=True)
    (stage_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    (stage_dir / "response.md").write_text(response, encoding="utf-8")


async def architect(page: str, goal: str, review_context: str = "") -> tuple[str, pathlib.Path]:
    """Run the Architect. Returns (response, spec_path)."""
    run_iter = len(list((RUNS_DIR / page).iterdir())) + 1 if (RUNS_DIR / page).exists() else 1
    run_dir = RUNS_DIR / page / f"iter-{run_iter:02d}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"  ARCHITECT → {page} (cycle {run_iter})")
    print(f"{'=' * 60}")

    spec_path = SPEC_DIR / f"{page}.md"

    feedback_block = ""
    if review_context:
        feedback_block = (
            "\n## Review feedback from previous cycle\n"
            "The previous build was rejected. Re-emit a tighter spec that addresses "
            "every BLOCKER below. Keep PASS items as-is.\n\n"
            f"{review_context}\n"
        )

    prompt = (
        f"Produce (or revise) the page spec for: {page}\n\n"
        f"Goal: {goal}\n\n"
        f"Read first: {BRAND_BRIEF}\n"
        f"Then read: {DESIGN_MD}\n"
        f"Existing build target (skim one page for context): {WEBSITE_DIR / (page + '.html')}\n"
        f"{feedback_block}"
        f"Write the spec to: {spec_path}\n"
        "Follow the schema in your Architect instructions exactly."
    )

    response = await run_agent("prompts.architect", prompt, label="ARCH")
    write_snapshot(run_dir, "architect", prompt, response)
    return response, spec_path


async def developer(page: str, spec_path: pathlib.Path) -> str:
    if not spec_path.exists():
        print(f"  ⚠ No spec found for {page}, skipping.")
        return ""

    page_run_dir = RUNS_DIR / page
    if not page_run_dir.exists():
        page_run_dir.mkdir(parents=True, exist_ok=True)
    run_iter = max(
        (int(p.name.split("-")[1]) for p in page_run_dir.iterdir() if p.is_dir() and p.name.startswith("iter-")),
        default=0,
    )
    run_dir = page_run_dir / f"iter-{run_iter:02d}"

    print(f"\n{'=' * 60}")
    print(f"  DEVELOPER → {page} (cycle {run_iter})")
    print(f"{'=' * 60}")

    spec = spec_path.read_text(encoding="utf-8")
    prompt = (
        f"Build the page: {page}\n\n"
        f"## Spec\n{spec}\n\n"
        f"Write the HTML file to: {WEBSITE_DIR / (page + '.html')}\n"
        f"Copy the shared nav and footer block verbatim from website/index.html, "
        "updating only the .active / aria-current link.\n"
        f"Write a BUILD_NOTES summary to {BUILD_DIR / (page + '.md')} after writing the HTML.\n"
        f"Read {BRAND_BRIEF} and {DESIGN_MD} before designing any section."
    )

    response = await run_agent("prompts.developer", prompt, label="DEV")
    write_snapshot(run_dir, "developer", prompt, response)
    return response


async def reviewer(page: str) -> str:
    page_run_dir = RUNS_DIR / page
    if not page_run_dir.exists():
        page_run_dir.mkdir(parents=True, exist_ok=True)
    run_iter = max(
        (int(p.name.split("-")[1]) for p in page_run_dir.iterdir() if p.is_dir() and p.name.startswith("iter-")),
        default=0,
    )
    run_dir = page_run_dir / f"iter-{run_iter:02d}"

    review_path = REVIEW_DIR / f"{page}.md"
    print(f"\n{'=' * 60}")
    print(f"  REVIEWER → {page} (cycle {run_iter})")
    print(f"{'=' * 60}")

    prompt = (
        f"Audit the page: {page}\n\n"
        f"Read {BRAND_BRIEF} and {DESIGN_MD} first.\n"
        f"Then read {WEBSITE_DIR / (page + '.html')} and every CSS file it links.\n"
        f"Write the review to: {review_path}\n"
        "Follow the schema in your Reviewer instructions exactly. "
        "Verdict must be exactly PASS, FAIL, or PASS WITH NOTES."
    )

    response = await run_agent("prompts.reviewer", prompt, label="REV")
    write_snapshot(run_dir, "reviewer", prompt, response)
    return response


def check_review_verdict(page: str) -> str:
    """Inspect the review file for verdict and parse blocker/nit lists."""
    review_path = REVIEW_DIR / f"{page}.md"
    if not review_path.exists():
        return "NO_REVIEW", "", ""
    text = review_path.read_text(encoding="utf-8")

    # Find verdict line
    verdict = "UNKNOWN"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Verdict"):
            continue
        if stripped in {"PASS", "FAIL", "PASS WITH NOTES"}:
            verdict = stripped
            break

    # Extract blockers / nits for the next cycle's Architect prompt
    blockers = ""
    nits = ""
    in_blockers = False
    in_nits = False
    for line in text.splitlines():
        if line.strip().startswith("## Blockers"):
            in_blockers = True
            in_nits = False
            continue
        if line.strip().startswith("## Nits"):
            in_nits = True
            in_blockers = False
            continue
        if line.strip().startswith("## "):
            in_blockers = False
            in_nits = False
            continue
        if in_blockers and line.strip():
            blockers += line + "\n"
        if in_nits and line.strip():
            nits += line + "\n"

    review_context = ""
    if blockers.strip():
        review_context += "### Blockers\n" + blockers
    if nits.strip():
        review_context += "### Nits (informational)\n" + nits
    return verdict, blockers.strip(), review_context


async def run_page(page: str) -> dict:
    result = {
        "page": page,
        "cycles": 0,
        "verdict": "",
        "blockers": "",
        "started_at": time.time(),
    }
    print(f"\n{'#' * 60}")
    print(f"  PIPELINE: {page}")
    print(f"{'#' * 60}")

    review_context = ""
    for cycle in range(1, MAX_CYCLES + 1):
        result["cycles"] = cycle

        # Stage 1: Architect (with feedback from prior cycle)
        await architect(page, PAGES[page]["goal"], review_context=review_context)

        # Stage 2: Developer
        spec_path = SPEC_DIR / f"{page}.md"
        code = await developer(page, spec_path)
        if not code:
            print(f"  ⚠ Developer produced no output for {page}")
            result["verdict"] = "FAILED_DEV"
            break

        # Stage 3: Reviewer
        await reviewer(page)
        verdict, blockers, review_context = check_review_verdict(page)
        result["verdict"] = verdict
        result["blockers"] = blockers

        if verdict == "PASS":
            print(f"\n  ✓ Page '{page}' passed review on cycle {cycle}")
            break
        if verdict == "PASS WITH NOTES":
            print(f"\n  ◐ Page '{page}' passed with notes on cycle {cycle}")
            break
        if verdict == "FAIL":
            if cycle < MAX_CYCLES:
                print(f"\n  ⚠ Review FAILED for '{page}' (cycle {cycle}/{MAX_CYCLES}). Re-Architecting...")
            else:
                print(f"\n  ✗ Page '{page}' still FAILING after {MAX_CYCLES} cycles.")

    result["elapsed_s"] = round(time.time() - result["started_at"], 1)
    print(f"\n  ✓ Pipeline complete for: {page} (verdict: {result['verdict']}, "
          f"cycles: {result['cycles']}, {result['elapsed_s']}s)")
    return result


async def run_all() -> list[dict]:
    results = []
    for page in PAGES:
        results.append(await run_page(page))
    return results


def print_summary(results: list[dict]) -> None:
    print(f"\n{'=' * 60}")
    print("  PIPELINE SUMMARY")
    print(f"{'=' * 60}")
    for r in results:
        v = r["verdict"]
        icon = "✓" if v == "PASS" else "◐" if "NOTES" in v else "✗"
        print(f"  {icon} {r['page']:>10}: {v:<20} cycles={r['cycles']}  {r['elapsed_s']}s")
    all_ok = all(r.get("verdict") in {"PASS", "PASS WITH NOTES"} for r in results)
    print(f"\n  Overall: {'ALL GREEN' if all_ok else 'NEEDS ATTENTION'}")
    print(f"  Run snapshots: {RUNS_DIR}")
    print(f"{'=' * 60}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ADW Pipeline Runner")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--all", action="store_true", help="Run all pages")
    group.add_argument("--page", choices=list(PAGES.keys()), help="Run one page")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without running")
    parser.add_argument("--cycles", type=int, default=MAX_CYCLES,
                        help=f"Max Architect→Develop→Review cycles per page (default {MAX_CYCLES})")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    global MAX_CYCLES
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    os.environ["GEMINI_API_KEY"] = api_key

    args = parse_args(argv)
    MAX_CYCLES = max(1, args.cycles)

    if args.dry_run:
        plan = {
            "pages": list(PAGES.keys()) if args.all else ([args.page] if args.page else []),
            "max_cycles": MAX_CYCLES,
            "stages_per_cycle": ["Architect", "Developer", "Reviewer"],
            "re_architect_on_fail": True,
            "snapshots": str(RUNS_DIR),
            "brand_brief": str(BRAND_BRIEF),
            "design_tokens": str(DESIGN_MD),
            "page_contracts": "BRAND_BRIEF.md §9",
        }
        print(json.dumps(plan, indent=2))
        return

    pages_to_run = list(PAGES.keys()) if args.all or not args.page else [args.page]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if len(pages_to_run) == 1:
            results = [loop.run_until_complete(run_page(pages_to_run[0]))]
            print_summary(results)
        else:
            results = loop.run_until_complete(run_all())
            print_summary(results)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
