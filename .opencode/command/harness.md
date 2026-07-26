---
description: Run the Google Antigravity harness. Usage: /harness --aura "prompt" or /harness -r "question"
agent: build
model: gemini/gemini-3.6-flash
---

<role>You run the Google Antigravity agent harness for the Aura project.</role>

<context>
The harness is at D:\PROJECTS\Harness\SDK\agent_harness.py
Usage: python agent_harness.py --aura "prompt" for Aura website work
       python agent_harness.py -r "question" for read-only queries
       python agent_harness.py --show-prompt --aura to debug the system prompt
</context>

<instructions>
Run the harness with the appropriate flags based on the user's request.

If the user wants to build or edit website files:
  python agent_harness.py --aura "{FOR NEEDED UDERSTAND TEH GOAL }"

If the user wants to ask a question or research:
  python agent_harness.py --aura -r "{FOR NEEDED UDERSTAND TEH GOAL }"

If the user wants to debug the prompt:
  python agent_harness.py --show-prompt --aura
</instructions>
