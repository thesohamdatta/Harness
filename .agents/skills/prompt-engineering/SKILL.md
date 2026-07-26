# Prompt Engineering — Harness SDK

Write system prompts for the google-antigravity harness using these principles.
Based on Anthropic's 2026 context engineering guidance.

## Structure

Every prompt follows the same XML-tagged skeleton:

```
<role>What the agent is</role>

<context>What the agent needs to know — project, stack, constraints</context>

<references>External files or docs the agent should read</references>

<instructions>What the agent does — numbered, positive, minimal</instructions>

<output>What the agent produces — shape, format, destination</output>
```

## Rules

1. **Say what to do, not what to avoid.** Positive instructions outperform prohibitions.
   - Good: "Animate transform/opacity only"
   - Bad: "Never use transition: all"

2. **Context before instructions.** Long material at top, ask at bottom.

3. **Minimal boilerplate.** Modern models are over-constrained. Delete any line that
   doesn't change behavior vs. default. Hunt no-ops sentence by sentence.

4. **One role per prompt.** Each agent config has exactly one role identity.

5. **Progressive disclosure.** Put inline what every session needs; push reference
   material into `<references>` blocks that point to files.

6. **Scope explicitly.** If a rule applies to all sections, say so. Modern models
   won't generalize from one item to the rest.
