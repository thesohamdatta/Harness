---
name: apple-hig
description: >
  Precise Apple HIG reference for exact measurements, platform-specific guidelines,
  and authoritative design principles. Use when you need to cite specific HIG
  requirements, measurements, or platform conventions with direct references to
  source documentation.
---

# Apple HIG Skill

Reference 156 distilled HIG files via the routing index to provide exact,
citable guidance from Apple's Human Interface Guidelines.

## How to Use This Skill

Follow these steps when applying the Apple HIG skill:

### 1. Parse the Request

Identify from the user's query:

- **Platform(s):** ios / ipados / macos / tvos / visionos / watchos
- **Components or patterns** mentioned (buttons, tab bars, sheets, etc.)
- **Frameworks or SDKs** referenced (HealthKit, SiriKit, ARKit, etc.)
- **Task type:** design / review / spec / audit / guidance

_Completion criterion: You can list all relevant platforms, components, frameworks, and task type from the request._

### 2. Load Tier 1 Foundations (Always)

Load these 16 universal foundation files before proceeding:
`accessibility`, `branding`, `color`, `dark-mode`, `design-principles`,
`icons`, `images`, `inclusion`, `layout`, `materials`, `motion`,
`privacy`, `right-to-left`, `sf-symbols`, `typography`, `writing`

_Completion criterion: All 16 tier-1 files are loaded and ready for reference._

### 3. Load Platform File (If Applicable)

For each detected platform, load its `designing-for-[platform]` file.
If "game" or "gaming" is mentioned, also load `designing-for-games`.

_Completion criterion: All relevant platform-specific overview files are loaded._

### 4. Scan for Tier 3 Matches

Normalize the request to lowercase and scan against the trigger map.
Load every matching tier-3 file (components, patterns, technologies).
Match only standalone words/phrases/API symbols - never partial matches.
Load each file at most once.

_Completion criterion: All relevant tier-3 files are loaded with no duplicates._

### 5. Expand Related Files (One Hop)

For each loaded tier-2 and tier-3 file, read its `related:` frontmatter.
Load any listed files not yet loaded - one hop only.

_Completion criterion: All relevant related files from tiers 2 and 3 are loaded._

### 6. Load Tier 4 On-Demand (If Needed)

Check the tier-4 trigger map for direct keyword matches.
Load tier-4 files only on direct keyword match or if named in a loaded file's `related:` list.
Avoid broad loading - these are niche, platform-specific controls.

_Completion criterion: Only specifically matched tier-4 files are loaded._

### 7. Provide Answer with Exact Citations

Apply all loaded content to answer the query.
Cite exact values (pt sizes, pixel densities, margins, timing values) as they appear in sources.
When platform behaviors differ, state each platform's rule explicitly.
Never invent - every rule, measurement, and API must trace to a loaded distilled file.
If uncertain, name the specific source file that would cover the topic.
Be terse and direct - state the rule without pedagogical framing.

_Completion criterion: Answer is provided with exact citations from loaded HIG sources, following all non-negotiables._

## Non-Negotiables (Apply These Rules)

- **Cite exact values.** State measurements, densities, timing values precisely as documented - never approximate.
- **Distinguish platforms.** When behaviors differ across platforms, state each platform's rule explicitly - never generalize.
- **No invention.** Every guideline, measurement, or API name must trace to a loaded distilled file. If unsure, name the source file.
- **Terse and direct.** This is a reference skill - state the rule plainly without tutorial explanations or pedagogical framing.

## File Reference

- Distilled reference files: `distilled/[topic].md`
- Routing index: `routing-index.md` (auto-generated from frontmatter)
- Frontmatter schema: Each distilled file contains `topic`, `tier`, `platforms`, `category`, `triggers`, and `related` fields.
