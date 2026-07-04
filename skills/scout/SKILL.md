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
| `/scout <topic or task>` | 3–4 parallel sweep agents + verifier | default — new domain, new project, radar fire |
| `/scout deep <topic>` | Workflow: 6 lenses + completeness critic, loop until dry | high-stakes coverage; user accepts the token cost |
| `/scout debrief <slug>` | inline, no sweep | post-implementation: fold deviations and implementation notes back into an existing brief as a dated delta |

## Protocol (standard mode)

0. **Scope + ledger.** Name the domain and the task it serves. Check `~/.claude/state/scout/domains.json`
   and grep `~/kb/` (vault-first rule). Scouted <30d ago → surface the existing
   brief, run a delta pass only. Well-covered by an existing KB → say so and stop.
1. **Fingerprint.** Decompose the task into the 2–5 fields it actually touches
   (e.g. "beautiful landing page" → motion design, typography, layout systems, perceived performance).
   If the task touches an existing codebase or project, the local repo IS part of the territory —
   flag it for the Territory lens.
2. **Sweep — blind angles.** Spawn parallel research agents, one per lens, prompts from
   [METHOD.md](METHOD.md): **Lexicon & Map** (terms of art + taxonomy), **Tools & Resources**
   (canonical stack, curated indexes, communities), **Tribal Knowledge** (practitioner heuristics,
   traps, amateur-vs-pro markers), plus **Territory** (local blindspot pass over the repo — only
   when a codebase is in play). Each agent is blind to the others. `deep` mode adds **Adjacents**
   and **Elder** as separate lenses plus a completeness critic, via the Workflow tool.
3. **Gap diff — four quadrants.** Compare sweep output against existing kb/memory/work-vault
   coverage (cite paths checked). Separate already-known from net-new, then classify each net-new
   gap: **known unknown** (a question you knew to ask), **unknown unknown** (net-new from the
   sweep), or **unknown known** (tacit context only the user holds — feed these to step 5's
   interview). Rank by leverage on the current task.
4. **Brief.** Compile to the template in METHOD.md → file per `~/kb/scout/.claude/CLAUDE.md`
   (raw deposit, wiki compile, _index bump, log entry). Cross-link `[[wikilinks]]` into topic KBs.
5. **Interview — unknown knowns.** Draft 3–5 prioritized questions for the *user*, ordered by how
   much the answer would change the approach (architecture-altering first). None should be
   answerable by web search — that's the sweep's job. Interactive session → ask via
   AskUserQuestion; autonomous → file under "Questions for you" in the brief. Half the territory
   is context only the user holds; no sweep agent can find it.
6. **Surface + route.** In conversation: top 5 gaps, one line each, with a routed next action
   (table below); close with the brief's **prompt scaffold** — a ready-to-paste context block for
   the follow-on prompt or plan. Update the ledger; optionally append top gaps to a Meridian-style inbox if you run one (formats in METHOD.md).
7. **Verify.** Spawn the `verifier` agent: rubric `~/.claude/rubrics/scout-brief.md`, artifact =
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
| After the build: fold what the walk taught you back into the map | `/scout debrief <slug>` |

*(Routes name skills from the author's setup — substitute your closest equivalents.)*

## Rules

- **Vault first, always.** Never re-scout what `~/kb/` already covers — delta passes only, cite the hits.
- **Radar fires are tripwires, not verdicts.** On a `<scout-radar>` note: check ledger + kb; if covered
  or routine, stay completely silent about scout. If genuinely new, offer `/scout "<domain>"` in ONE line.
- **Brief ≠ tutorial.** Optimize for *naming* things precisely and linking out; depth is other skills' job.
- **Sources or it didn't happen.** Every resource gets a URL; every claim a source; agents report their angle.
- **Never self-certify** — verifier + rubric on every filed brief (quick and debrief modes exempt from a fresh verify: quick files nothing; debrief appends to an already-verified brief).
- **Propose, don't promote.** The brief and conversation surface gaps; the user decides what gets pursued.
- **Better prompts, not just briefs.** The end product is a sharper follow-on prompt. The scaffold
  states known knowns, flags open known unknowns, and attaches references — source code beats
  screenshots, because downstream agents read code, not pixels.
- **Specificity balance.** Enough context to avoid generic output; not so much prescription that a
  flawed approach gets locked in. State the starting point and experience level; leave the *how*
  loosest where certainty is lowest.

Sweep-agent prompts, brief template, ledger/inbox formats, deep-mode workflow: [METHOD.md](METHOD.md)
