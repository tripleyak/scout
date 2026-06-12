# Knowledge Base: Scout — domain maps & unknown-unknown briefs

> You are the compiler. This KB holds domain briefs produced by the `scout` skill
> (`~/.claude/skills/scout/SKILL.md`). Silent writes permitted — briefs file without asking.

## Directory Structure

```
raw/          Lens outputs from sweep agents (one file per scout run: <slug>-lenses.md)
wiki/         Compiled briefs (YOU maintain this)
  _index.md   Master index — always keep current
  <slug>.md   One brief per scouted domain
  log.md      Dated compile log
```

## Article Template

The brief template lives in `~/.claude/skills/scout/METHOD.md` — frontmatter (title, date,
domain, task_context, depth) + 10 sections (TL;DR, Vocabulary, Map, Canonical resources,
Tribal knowledge, Options landscape, Questions you didn't know to ask, Gap diff, Next
actions, Sources). Briefs are graded against `~/.claude/rubrics/scout-brief.md`.

## Compilation Rules

1. One brief per domain. Re-scouting an existing domain = **delta pass**: update the existing
   brief, add a `## Delta YYYY-MM-DD` section, never fork a near-duplicate.
2. Deposit raw lens outputs to `raw/<slug>-lenses.md` before compiling; never edit raw/ after write.
3. Cross-link `[[wikilinks]]` into topic KBs when one covers the domain (e.g. a design brief
   links into `claude-design`); cite as relative vault links.
4. Update `_index.md` and append to `log.md` (`## [YYYY-MM-DD] scout | <domain>`) on every run.
5. After filing, update the ledger `~/.claude/state/scout/domains.json` and optionally append ≤3 gap
   candidates to a Meridian-style inbox if you run one (formats in METHOD.md).
6. Lint = grade a sample brief against the rubric with the `verifier` agent.

## Query Protocol

"Have we scouted X?" → check `_index.md`, then the ledger. Answer with the brief path and
its date; offer a delta pass if >30 days old or the task context differs materially.
