# Rubric: scout domain brief

Grades briefs produced by the scout skill (`~/.claude/skills/scout/SKILL.md`); template in
`~/.claude/skills/scout/METHOD.md`. Artifact = the wiki brief at `~/kb/scout/wiki/<slug>.md`.

## Coverage
- Vocabulary table contains ≥15 domain-specific terms of art, each with a definition AND a
  why-it-matters-here note. Generic software/common words ("API", "framework", "the internet")
  don't count toward the 15.
- Map section organizes the domain into ≥4 named categories with at least one concrete example
  each, plus explicit decision axes.
- Canonical resources section lists ≥5 resources with URLs, including ≥1 curated index
  (awesome-list / gallery / survey / glossary) and ≥1 practitioner community.
- Tribal-knowledge section lists ≥5 practitioner heuristics, traps, or failure modes that are
  not restatements of tool documentation.

## Gap focus
- "Questions you didn't know to ask" section contains ≥5 questions, each naming the concept
  that unlocks it.
- "Questions for you" section contains 3–5 questions only the user can answer, ordered by how
  much the answer would change the approach; none is answerable by web search.
- Gap diff cites the actual paths checked in `~/kb/` and memory,
  separates already-known items from net-new ones, and tags each net-new gap with its quadrant
  (known-unknown / unknown-unknown / unknown-known).
- Options landscape names 2–4 viable approaches for the triggering task with tradeoffs, using
  terms defined in the vocabulary section.
- (only when the Territory lens ran) Local-territory section cites file:line for the modules,
  conventions, prior art, and off-limits abstractions it names.

## Grounding
- Every resource has a URL; load-bearing claims carry sources; the Sources section lists each
  sweep lens that ran and its angle.
- (advisory) Spot-check 3 resource URLs — they resolve and match their description.

## Actionability
- Next-actions table routes each surfaced gap to a concrete skill or tool (per the SKILL.md
  routing table), not "research further".
- TL;DR states the single highest-leverage unknown and a recommended next action in ≤3 lines.
- Prompt scaffold is a self-contained, ready-to-paste context block: states the known knowns,
  flags the open known-unknowns, lists references (source code first), names the starting
  point/experience level, and notes where specificity is deliberately left loose.
- (advisory) Watch-list names 3–5 unknowns likely to surface during implementation, each paired
  with the signal that would reveal it.

## Output Quality
- Brief exists at `~/kb/scout/wiki/<slug>.md` with template frontmatter (title, date, domain,
  task_context, depth); raw lens outputs deposited under `~/kb/scout/raw/`; `_index.md` bumped;
  dated entry appended to `wiki/log.md`.
- Ledger `~/.claude/state/scout/domains.json` has the domain entry pointing at the brief.
- (only if a Meridian inbox exists) `~/.claude/state/meridian/inbox.md` gained ≤3 `- [ ] **scout** | ...` candidates
  under a dated scout header (propose-only; no other inbox lines modified or removed).
