"""
Google Antigravity dev harness — wraps Agent for CLI-driven interactions.

Usage:
    python agent_harness.py --aura "add an FAQ section"
    python agent_harness.py -w . --read-only "list all files"
    python agent_harness.py --show-prompt --aura             # debug prompt
    python workflows/adw-pipeline.py --all                   # multi-agent
"""

import argparse
import asyncio
import os
import sys

from google.antigravity import Agent
from google.antigravity.connections.local import LocalAgentConfig
from google.antigravity.types import BuiltinTools, CapabilitiesConfig


def create_config(
    *,
    model: str = "gemini-3.6-flash",
    workspace: str | None = None,
    system_instructions: str | None = None,
    read_only: bool = False,
    api_key: str | None = None,
) -> LocalAgentConfig:
    capabilities = (
        CapabilitiesConfig(enabled_tools=BuiltinTools.read_only())
        if read_only
        else None
    )
    workspaces = [workspace] if workspace else None
    return LocalAgentConfig(
        model=model,
        api_key=api_key,
        system_instructions=system_instructions,
        workspaces=workspaces,
        capabilities=capabilities,
    )


async def run(prompt: str, config: LocalAgentConfig) -> None:
    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        async for token in response:
            print(token, end="", flush=True)
        print()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Google Antigravity dev harness"
    )
    parser.add_argument("prompt", nargs="*", help="Prompt text")
    parser.add_argument("--model", default="gemini-3.6-flash")
    parser.add_argument("--workspace", "-w", help="Workspace directory")
    parser.add_argument("--show-prompt", action="store_true", help="Print the system prompt and exit")
    parser.add_argument("--system", "-s", help="System instructions file path")
    parser.add_argument("--read-only", "-r", action="store_true")
    parser.add_argument("--aura", action="store_true", help="Use Aura config")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    api_key = os.environ.get("GEMINI_API_KEY")

    if args.aura:
        import prompts.aura
        config = prompts.aura.create_config(read_only=args.read_only)
        prompt = " ".join(args.prompt) if args.prompt else sys.stdin.read()
        if args.show_prompt:
            print("--- System Prompt ---")
            print(config.system_instructions or "(none)")
            print("---------------------")
            return
        if not api_key:
            print("Error: GEMINI_API_KEY not set", file=sys.stderr)
            sys.exit(1)
    else:
        if not api_key and not args.show_prompt:
            print("Error: GEMINI_API_KEY not set", file=sys.stderr)
            sys.exit(1)
        system_text = None
        if args.system:
            with open(args.system) as f:
                system_text = f.read()
        config = create_config(
            model=args.model,
            workspace=args.workspace or os.getcwd(),
            system_instructions=system_text,
            read_only=args.read_only,
            api_key=api_key,
        )
        prompt = " ".join(args.prompt) if args.prompt else sys.stdin.read()
        if args.show_prompt:
            print("── System Prompt ──")
            print(system_text or "(none)")
            print("───────────────────")
            return

    asyncio.run(run(prompt.strip(), config))


if __name__ == "__main__":
    main()
