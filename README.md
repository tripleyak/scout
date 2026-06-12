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
2. **Sweep** — `/scout <topic>` spawns parallel research agents that are blind to each other, each owning one lens: Lexicon & Map, Toolsmith, Elder (tribal knowledge). Diversity catches what redundancy can't.
3. **Brief** — ten sections filed to `~/kb/scout/wiki/`: vocabulary (≥15 terms), territory map, canonical resources, tribal knowledge, options landscape, the questions you didn't know to ask, routed next actions.
4. **Verify** — a fresh-context verifier grades the brief against the rubric. Required failures send it back.
5. **Compound** — the ledger grows; the radar reads it and gets quieter as your map gets larger.

Modes: `/scout quick <topic>` (inline, nothing filed) · `/scout <topic>` (standard) · `/scout deep <topic>` (5 lenses + completeness critic).

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
