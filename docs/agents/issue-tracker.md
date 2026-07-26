# Issue Tracker: Local Markdown

This repo uses **local markdown files** for issue tracking (no GitHub Issues, Jira, or Linear).

## Where issues live

```
.scratch/<effort-name>/
├── map.md                  # The wayfinder map (label: wayfinder:map)
└── tickets/
    ├── 001--ticket-title.md
    └── 002--another-ticket.md
```

## Labels

Labels are expressed as `tag:` prefixes in the file name or frontmatter:
- `ticket-type:research`, `ticket-type:prototype`, `ticket-type:grilling`, `ticket-type:task`
- `wayfinder:map` — the map itself

## Wayfinding operations

- **Map:** `.scratch/<effort>/map.md` — contains Decision, Destination, Not-yet-specified, Out-of-scope
- **Child tickets:** `.scratch/<effort>/tickets/<number>--<slug>.md`
- **Blocking:** Expressed as a `## Blocking` section in the ticket body referencing other ticket filenames
- **Frontier:** Open tickets not blocked by any other open ticket
- **Resolution:** Post resolution as a `## Resolution` section in the ticket body, then rename file to prefix with `closed-` or move to `tickets/closed/`
