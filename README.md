# Scout — map the territory before you walk it

An always-on **unknown-unknowns system** for [Claude Code](https://claude.com/claude-code). Scout converts unknown unknowns into known unknowns before you commit to an approach: the terms of art, taxonomies, canonical tools, named methods, and tribal knowledge of any domain — plus the questions you didn't know to ask.

**The story of how it was designed:** https://scout-site-gules.vercel.app (that's `index.html` in this repo)

## Install (one command)

```bash
curl -fsSL https://raw.githubusercontent.com/tripleyak/scout-site/master/install.sh | bash
```

Then **restart Claude Code** (skills load at session start) and try:

```
/scout "web animation and motion design"
```

Requirements: Claude Code, `python3`, `git`.

## What gets installed

| Piece | Where | Role |
|---|---|---|
| `/scout` skill (SKILL.md + METHOD.md) | `~/.claude/skills/scout/` | The brain — scoping, blind-lens sweeps, brief compilation, routing |
| Radar hook | `~/.claude/hooks/scout_radar.py` + registered in `settings.json` | Always-on regex tripwire on every prompt (<50ms, 1/session, 3/day caps) |
| Grading rubric | `~/.claude/rubrics/scout-brief.md` | Briefs are graded by a fresh-context verifier — never self-certified |
| Verifier agent | `~/.claude/agents/verifier.md` | Independent rubric grader (installed only if you don't already have one) |
| Knowledge base | `~/kb/scout/` (raw/, wiki/, outputs/ + compile protocol) | One brief per domain; re-scouts are delta passes, never duplicates |
| State | `~/.claude/state/scout/` | Ledger of scouted domains + radar rate-limit state (created empty) |

The installer is idempotent and backs up any existing `~/.claude/skills/scout/` before replacing it. It never overwrites knowledge-base content or your existing verifier agent.

## How it works

1. **Radar** — a deliberately dumb regex hook watches every prompt for uncertainty phrasing ("I don't even know what's possible") and new-endeavor signals. Cheap trigger, smart filter: the session model decides whether to surface anything.
2. **Sweep** — `/scout <topic>` spawns parallel research agents that are blind to each other, each owning one lens: Lexicon & Map, Toolsmith, Elder (tribal knowledge), plus a **Territory** lens that runs a blindspot pass over your local repo when the task touches a codebase. Diversity catches what redundancy can't.
3. **Interview** — the sweep only covers what the web can know. Scout then asks *you* 3–5 prioritized questions (architecture-altering first) to surface your unknown *knowns* — the tacit context no search can find.
4. **Brief** — fourteen sections filed to `~/kb/scout/wiki/`: vocabulary (≥15 terms), territory map, canonical resources, tribal knowledge, local territory (file:line), options landscape, the questions you didn't know to ask, a four-quadrant gap diff, a watch-list of unknowns likely to surface mid-build, and a ready-to-paste **prompt scaffold** for whatever prompt or plan comes next.
5. **Verify** — a fresh-context verifier grades the brief against the rubric. Required failures send it back.
6. **Compound** — the ledger grows; the radar reads it and gets quieter as your map gets larger. After you build, `/scout debrief <slug>` folds what the territory taught you back into the brief.

Modes: `/scout quick <topic>` (inline, nothing filed) · `/scout <topic>` (standard) · `/scout deep <topic>` (6 lenses + completeness critic) · `/scout debrief <slug>` (post-build delta).

## Lineage

Scout's blind-lens sweep is original; the four-quadrant unknowns frame (known/unknown × known/unknown), the local **blindspot pass**, the user **interview**, the **prompt scaffold** with its specificity-balance rule, and the debrief loop are adopted from Thariq Shihipar's ["A Field Guide to Fable: Finding Your Unknowns"](https://x.com/trq212/status/2073100352921215386) (July 2026). His thesis — the map is not the territory, and output quality is bounded by how well you discover your own unknowns before prompting — is exactly the job scout automates.

## Sibling system

**[Genome](https://github.com/tripleyak/genome-site)** — scout maps territory ahead; genome dissects ideas behind (12-layer idea autopsies → generative principles).

## Uninstall

```bash
rm -rf ~/.claude/skills/scout ~/.claude/hooks/scout_radar.py ~/.claude/rubrics/scout-brief.md
# then remove the scout_radar.py entry from hooks.UserPromptSubmit in ~/.claude/settings.json
# your briefs in ~/kb/scout/ are yours — delete only if you want to
```

## License

MIT
