# Scout method — lenses, prompts, formats

## Why lenses

One searcher finds what it searches for. Unknown unknowns hide in the angles you didn't take,
so the sweep runs multiple agents that are **blind to each other**, each owning one way of
seeing a domain. Diversity catches what redundancy can't.

## The four quadrants

The map (your prompt and context) never equals the territory (the domain plus your actual
codebase). Gaps between them come in four kinds — frame after Thariq Shihipar's
["A Field Guide to Fable: Finding Your Unknowns"](https://x.com/trq212/status/2073100352921215386):

| | You know it | You don't know it |
|---|---|---|
| **Aware of it** | Known knowns — state them in the prompt scaffold | Known unknowns — open questions; flag them explicitly |
| **Unaware of it** | Unknown knowns — tacit context; only the *interview* surfaces it | Unknown unknowns — the *sweep's* job |

The sweep hunts the bottom-right quadrant; the interview hunts the bottom-left; the prompt
scaffold packages the top row for whatever prompt or plan comes next. A scout that only sweeps
covers one quadrant of four.

## The six lenses

| Lens | Owns | Standard mode |
|---|---|---|
| **Lexicon** | Terms of art, named effects/patterns/algorithms/methods, jargon, search vocabulary | merged with Map |
| **Map** | Taxonomy: schools, categories, decision axes; how practitioners segment the field | agent 1 |
| **Toolsmith** | Canonical tools/libraries/standards, curated indexes (awesome-lists, galleries, surveys, glossaries), communities | agent 2 |
| **Elder** | Tribal knowledge: heuristics, traps, failure modes, "what nobody tells beginners", amateur-vs-pro markers | agent 3 |
| **Territory** | The local codebase/project: modules the task touches, conventions, invariants, prior art, abstractions the approach must respect | agent 4 — only when a repo is in play |
| **Adjacents** | Neighboring fields with transferable vocabulary/methods (deep mode only) | — |

## Sweep agent prompt template

Each agent gets web access (WebSearch/WebFetch) and returns raw data, not prose for humans —
except the **Territory** lens, which gets repo access (Read/Grep/Glob) instead of the web.
Fill `{domain}`, `{task}`, `{lens block}`:

Lens sweeps are volume work, not judgment — the prompt fully determines the outcome, so spawn
each sweep agent on a cheap model (e.g. `Agent(model: "sonnet")`). Synthesis, the gap diff, the
interview, and all verdicts stay with the session model: spend the expensive model on judgment,
cheap models on volume.

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
  Discord, forum, conference); the 2–3 reference implementations or showcases people copy.
  Prefer source-code references (repos) over screenshots, demos, or marketing pages —
  downstream agents read code, not pixels."
- **Elder**: "Return tribal knowledge: practitioner heuristics and rules of thumb; the traps
  and failure modes beginners hit; 'nobody tells you X' facts; what separates amateur from
  professional work in this field (taste markers); which 'best practices' are actually cargo
  cult; what the experts argue about."
- **Territory** (only when a repo/project is in play — repo access, not web): "Run a blindspot
  pass over {repo path} for this task. Return: (a) the modules/files the task will touch;
  (b) the conventions and invariants they encode — naming, layering, error handling, test
  patterns; (c) prior art — existing code that already solves part of the task; (d) abstractions
  the approach must not duplicate or violate; (e) 3–5 repo-specific questions the implementer
  should answer before writing code. Cite file:line for every claim."
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
6. **Local territory** *(only when the Territory lens ran)* — modules the task touches,
   conventions/invariants, prior art, off-limits abstractions — every claim with file:line.
7. **Options landscape for this task** — the 2–4 viable approaches with tradeoffs, in terms the
   vocabulary section defined.
8. **Questions you didn't know to ask** — ≥5 unknown unknowns, each naming the concept that unlocks it.
9. **Questions for you** — 3–5 unknown *knowns*: prioritized questions only the user can answer,
   architecture-altering first, none answerable by web search. Record answers inline when given.
10. **Gap diff** — paths checked in ~/kb/ + memory; already-known vs net-new; each net-new gap
    tagged with its quadrant (known-unknown / unknown-unknown / unknown-known).
11. **Watch-list** — 3–5 unknowns likely to surface only *during* implementation, each with the
    signal that would reveal it (a test that fails, a module that resists, a number that looks off).
12. **Prompt scaffold** — a ready-to-paste context block for the follow-on prompt/plan: the known
    knowns worth stating, the open known-unknowns to flag, references to attach (source code
    first), the user's starting point/experience level, and a one-line note on where specificity
    is deliberately left loose (specificity balance: over-prescription locks in flawed approaches,
    vagueness produces generic output). When the follow-on is a *delegated build* — an implementer
    agent or a context-free session — shape the scaffold as a five-part spec instead: objective,
    files, interfaces, constraints, verification command. It must survive without this conversation.
13. **Next actions** — table: gap | routed skill/tool (from SKILL.md routing table).
14. **Sources** — per-lens agent angle + URLs.

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

## Debrief mode — feed the walk back into the map

`/scout debrief <slug>` runs after implementation, when the territory has taught you things the
sweep couldn't. Inputs: the existing brief + whatever deviation records exist (an
`implementation-notes.md`, the PR description, `git log`, or the user's own account). No sweep
agents, no fresh verify. Append a dated **Debrief** section to the brief:

- which watch-list items actually fired (and which never did — miscalibration is data too);
- which prompt-scaffold assumptions the territory contradicted;
- net-new vocabulary, traps, and heuristics learned only by walking;
- one line: what the *next* scout of an adjacent domain should do differently.

Bump the ledger entry's `scouted` date and set `depth: debrief`. The map compounds only if the
walk feeds back into it.

## Deep mode — Workflow sketch

User saying `/scout deep` is the opt-in for the Workflow tool. Shape: phase 1 fans out all
lenses in parallel — the five research lenses plus Territory when a repo is in play (each via
`agent()` with the prompt template); phase 2 runs a completeness
critic ("what angle is missing — modality not run, claim unverified, community unchecked?");
critic findings spawn one more targeted round (loop until dry, max 2 extra rounds); phase 3 is a
single synthesis agent compiling the brief from all lens outputs. Then verify per SKILL.md step 7.

## Radar (always-on tripwire)

`~/.claude/hooks/scout_radar.py` on UserPromptSubmit: fires on explicit-uncertainty phrasing or
long new-endeavor prompts, max 1/session and 3/day, state in `~/.claude/state/scout/radar.json`.
It is deliberately dumb; the session model applies judgment per SKILL.md Rules. Tune the regexes
there if it over/under-fires — never add an LLM call to the hook path.
