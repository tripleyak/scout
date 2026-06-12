# Scout method — lenses, prompts, formats

## Why lenses

One searcher finds what it searches for. Unknown unknowns hide in the angles you didn't take,
so the sweep runs multiple agents that are **blind to each other**, each owning one way of
seeing a domain. Diversity catches what redundancy can't.

## The five lenses

| Lens | Owns | Standard mode |
|---|---|---|
| **Lexicon** | Terms of art, named effects/patterns/algorithms/methods, jargon, search vocabulary | merged with Map |
| **Map** | Taxonomy: schools, categories, decision axes; how practitioners segment the field | agent 1 |
| **Toolsmith** | Canonical tools/libraries/standards, curated indexes (awesome-lists, galleries, surveys, glossaries), communities | agent 2 |
| **Elder** | Tribal knowledge: heuristics, traps, failure modes, "what nobody tells beginners", amateur-vs-pro markers | agent 3 |
| **Adjacents** | Neighboring fields with transferable vocabulary/methods (deep mode only) | — |

## Sweep agent prompt template

Each agent gets web access (WebSearch/WebFetch) and returns raw data, not prose for humans.
Fill `{domain}`, `{task}`, `{lens block}`:

```
You are one blind lens in a multi-angle sweep of the domain "{domain}", serving this task:
"{task}". Other agents cover other angles — do NOT summarize the domain generally; own your
lens only. Search the live web; do not answer from memory alone. Every item needs a source URL.

{lens block}

Elicitation prompts to push past the obvious:
- What would a 10-year practitioner call this exact problem?
- What is the curated index everyone in this field actually references?
- What terms would someone need just to SEARCH this field effectively?
- What did this field call this concept 10 years ago vs now?
- What do beginners reliably get wrong in their first month?

Return structured markdown lists, dense, no preamble. Minimum 15 items for vocabulary lenses,
8 for others. Mark anything you suspect is contested or stale.
```

Lens blocks:

- **Lexicon & Map**: "Return (a) a vocabulary table — term | 1-line definition | why it matters
  for the task — covering terms of art, named techniques/effects/patterns/algorithms; (b) a
  taxonomy of the field: the 4–8 named categories or schools practitioners use to divide it,
  with one canonical example each, plus the 3–5 decision axes that distinguish approaches."
- **Toolsmith**: "Return the canonical stack: tools, libraries, standards, and services
  practitioners actually use NOW (note what's fading); at least one awesome-list/gallery/
  survey/glossary-style curated index; the communities where the field talks (subreddit,
  Discord, forum, conference); the 2–3 reference implementations or showcases people copy."
- **Elder**: "Return tribal knowledge: practitioner heuristics and rules of thumb; the traps
  and failure modes beginners hit; 'nobody tells you X' facts; what separates amateur from
  professional work in this field (taste markers); which 'best practices' are actually cargo
  cult; what the experts argue about."
- **Adjacents** (deep): "Return 3–5 neighboring fields that solved analogous problems, and for
  each: the transferable concept, its name in that field, and one source to steal from."

## Brief template

File: `~/kb/scout/wiki/<slug>.md` (slug: kebab-case domain). Frontmatter:

```yaml
---
title: "Scout brief: <domain>"
date: YYYY-MM-DD
domain: <domain>
task_context: "<the task that triggered the scout>"
depth: quick | standard | deep
---
```

Sections, in order (rubric `~/.claude/rubrics/scout-brief.md` grades these):

1. **TL;DR** — 3 lines: what this territory is, the single highest-leverage thing you didn't
   know to ask about, and the recommended next action.
2. **Vocabulary** — table: term | what it is | why it matters here. ≥15 domain-specific terms of art.
3. **Map of the territory** — the taxonomy (≥4 named categories, one example each) + decision axes.
4. **Canonical resources** — ≥5 with URLs; must include ≥1 curated index and ≥1 practitioner community.
5. **Tribal knowledge & traps** — ≥5 practitioner heuristics/failure modes not in tool docs.
6. **Options landscape for this task** — the 2–4 viable approaches with tradeoffs, in terms the
   vocabulary section defined.
7. **Questions you didn't know to ask** — ≥5, each naming the concept that unlocks it.
8. **Gap diff** — paths checked in ~/kb/ + memory; already-known vs net-new.
9. **Next actions** — table: gap | routed skill/tool (from SKILL.md routing table).
10. **Sources** — per-lens agent angle + URLs.

## Ledger format — `~/.claude/state/scout/domains.json`

```json
{ "<slug>": { "scouted": "YYYY-MM-DD", "brief": "~/kb/scout/wiki/<slug>.md", "depth": "standard" } }
```

Update on every filed brief. The radar hook reads this to list covered domains in its note.

## Meridian inbox append (optional) — `~/.claude/state/meridian/inbox.md`

Skip this section if you don't run a Meridian-style inbox.

Propose-only, matching the harvest format (collector counts `^- [ ]`):

```
## YYYY-MM-DD (scout: <domain>)
- [ ] **scout** | <domain>: <gap, one line> | why: <leverage for the active task>
```

Top 3 gaps max per scout — the inbox is for things the user should decide to pursue, not the whole brief.

## Deep mode — Workflow sketch

User saying `/scout deep` is the opt-in for the Workflow tool. Shape: phase 1 fans out all five
lenses in parallel (each via `agent()` with the prompt template); phase 2 runs a completeness
critic ("what angle is missing — modality not run, claim unverified, community unchecked?");
critic findings spawn one more targeted round (loop until dry, max 2 extra rounds); phase 3 is a
single synthesis agent compiling the brief from all lens outputs. Then verify per SKILL.md step 6.

## Radar (always-on tripwire)

`~/.claude/hooks/scout_radar.py` on UserPromptSubmit: fires on explicit-uncertainty phrasing or
long new-endeavor prompts, max 1/session and 3/day, state in `~/.claude/state/scout/radar.json`.
It is deliberately dumb; the session model applies judgment per SKILL.md Rules. Tune the regexes
there if it over/under-fires — never add an LLM call to the hook path.
