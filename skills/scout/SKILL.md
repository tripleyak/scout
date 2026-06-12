---
name: scout
description: Map a domain's unknown unknowns before committing to an approach — terms of art, taxonomies, canonical tools and libraries, named methods, tribal knowledge, and the questions you didn't know to ask. Produces a verifier-graded domain brief filed to ~/kb/scout/ plus routed gap candidates. Use when starting work in an unfamiliar domain or new project, before /ce-plan, /ce-brainstorm, or design work, when the user says "scout", "what am I missing", "what don't I know", "what's possible", "map the territory", or "unknown unknowns", or when a <scout-radar> context note fires.
---

# Scout — map the territory before you walk it

Goal: convert unknown unknowns into known unknowns. The deliverable is a **domain brief** —
vocabulary, territory map, canonical resources, tribal knowledge, and routed next actions —
NOT an answer to the task. Scout names things; other skills resolve them.

## Modes

| Invocation | Depth | Use |
|---|---|---|
| `/scout quick <topic>` | inline, no subagents | mid-task micro-scout of one concept cluster; ~10-line vocabulary + resources reply, no brief filed |
| `/scout <topic or task>` | 3 parallel sweep agents + verifier | default — new domain, new project, radar fire |
| `/scout deep <topic>` | Workflow: 5 lenses + completeness critic, loop until dry | high-stakes coverage; user accepts the token cost |

## Protocol (standard mode)

0. **Scope + ledger.** Name the domain and the task it serves. Check `~/.claude/state/scout/domains.json`
   and grep `~/kb/` (vault-first rule). Scouted <30d ago → surface the existing
   brief, run a delta pass only. Well-covered by an existing KB → say so and stop.
1. **Fingerprint.** Decompose the task into the 2–5 fields it actually touches
   (e.g. "beautiful landing page" → motion design, typography, layout systems, perceived performance).
2. **Sweep — blind angles.** Spawn parallel research agents, one per lens, prompts from
   [METHOD.md](METHOD.md): **Lexicon & Map** (terms of art + taxonomy), **Tools & Resources**
   (canonical stack, curated indexes, communities), **Tribal Knowledge** (practitioner heuristics,
   traps, amateur-vs-pro markers). Each agent is blind to the others. `deep` mode adds **Adjacents**
   and **Elder** as separate lenses plus a completeness critic, via the Workflow tool.
3. **Gap diff.** Compare sweep output against existing kb/memory/work-vault coverage (cite paths
   checked). Separate already-known from net-new; rank net-new by leverage on the current task.
4. **Brief.** Compile to the template in METHOD.md → file per `~/kb/scout/.claude/CLAUDE.md`
   (raw deposit, wiki compile, _index bump, log entry). Cross-link `[[wikilinks]]` into topic KBs.
5. **Surface + route.** In conversation: top 5 gaps, one line each, with a routed next action
   (table below). Update the ledger; optionally append top gaps to a Meridian-style inbox if you run one (formats in METHOD.md).
6. **Verify.** Spawn the `verifier` agent: rubric `~/.claude/rubrics/scout-brief.md`, artifact =
   the brief. Fix required failures once; never self-certify.

## Routing resolved gaps

| Gap type | Route |
|---|---|
| Need to understand a concept | `teach` / `learn` skill |
| Stress-test understanding | `grill-with-docs` / `grill-me` |
| What practitioners use/discuss right now | `/signalsweep <topic>` |
| Deep multi-source dive on one question | `deep-research` skill |
| Library/API specifics | Context7 (`resolve-library-id` → `get-library-docs`) |
| Apply to design work | `ce-frontend-design` / `/design-html` with the brief as context |
| Plan the build | `compound-engineering:ce-plan` — feed it the brief |
| Visualize the territory | `excalidraw-diagram` from the brief's map section |
| Dissect a specific novel idea (not a domain) | `/genome <idea>` — sibling skill; harvest the generative principle |

*(Routes name skills from the author's setup — substitute your closest equivalents.)*

## Rules

- **Vault first, always.** Never re-scout what `~/kb/` already covers — delta passes only, cite the hits.
- **Radar fires are tripwires, not verdicts.** On a `<scout-radar>` note: check ledger + kb; if covered
  or routine, stay completely silent about scout. If genuinely new, offer `/scout "<domain>"` in ONE line.
- **Brief ≠ tutorial.** Optimize for *naming* things precisely and linking out; depth is other skills' job.
- **Sources or it didn't happen.** Every resource gets a URL; every claim a source; agents report their angle.
- **Never self-certify** — verifier + rubric on every filed brief (quick mode exempt: nothing is filed).
- **Propose, don't promote.** The brief and conversation surface gaps; the user decides what gets pursued.

Sweep-agent prompts, brief template, ledger/inbox formats, deep-mode workflow: [METHOD.md](METHOD.md)
