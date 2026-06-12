#!/usr/bin/env bash
# Scout installer — unknown-unknowns mapping system for Claude Code.
# Usage (one-liner):
#   curl -fsSL https://raw.githubusercontent.com/tripleyak/scout-site/master/install.sh | bash
# Or from a clone:  bash install.sh
set -euo pipefail

REPO_URL="https://github.com/tripleyak/scout-site.git"
NAME="scout"

# Self-bootstrap: when piped via curl there is no repo on disk — clone it and re-exec.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-.}")" 2>/dev/null && pwd || echo "")"
if [ -z "$SCRIPT_DIR" ] || [ ! -d "$SCRIPT_DIR/skills/$NAME" ]; then
  command -v git >/dev/null || { echo "git is required"; exit 1; }
  TMP="$(mktemp -d)"
  echo "→ Cloning $REPO_URL ..."
  git clone --quiet --depth 1 "$REPO_URL" "$TMP/repo"
  exec bash "$TMP/repo/install.sh"
fi

command -v python3 >/dev/null || { echo "python3 is required"; exit 1; }

CLAUDE="$HOME/.claude"
KB="$HOME/kb/$NAME"
TS="$(date +%Y%m%d%H%M%S)"

echo "→ Installing $NAME into $CLAUDE and $KB"
mkdir -p "$CLAUDE/skills" "$CLAUDE/hooks" "$CLAUDE/rubrics" "$CLAUDE/agents" \
         "$CLAUDE/state/scout" "$CLAUDE/state/genome"

# Skill (back up any existing copy first)
if [ -d "$CLAUDE/skills/$NAME" ]; then
  cp -R "$CLAUDE/skills/$NAME" "$CLAUDE/skills/$NAME.bak-$TS"
  echo "  existing skill backed up → skills/$NAME.bak-$TS"
fi
rm -rf "$CLAUDE/skills/$NAME"
cp -R "$SCRIPT_DIR/skills/$NAME" "$CLAUDE/skills/"
echo "  skill → ~/.claude/skills/$NAME/"

# Radar hook (shared with genome — same file, idempotent)
cp "$SCRIPT_DIR/hooks/scout_radar.py" "$CLAUDE/hooks/scout_radar.py"
echo "  hook  → ~/.claude/hooks/scout_radar.py"

# Rubric + verifier agent (verifier only if absent — don't clobber a customized one)
cp "$SCRIPT_DIR/rubrics/scout-brief.md" "$CLAUDE/rubrics/"
echo "  rubric → ~/.claude/rubrics/scout-brief.md"
if [ ! -f "$CLAUDE/agents/verifier.md" ]; then
  cp "$SCRIPT_DIR/agents/verifier.md" "$CLAUDE/agents/"
  echo "  agent → ~/.claude/agents/verifier.md"
fi

# Knowledge-base scaffold (never overwrites existing content)
mkdir -p "$KB/raw" "$KB/wiki" "$KB/outputs" "$KB/.claude"
[ -f "$KB/.claude/CLAUDE.md" ] || cp "$SCRIPT_DIR/kb-template/.claude/CLAUDE.md" "$KB/.claude/"
[ -f "$KB/wiki/_index.md" ] || printf '# Scout briefs — index\n\nNo domains scouted yet. Run `/scout "<domain>"`.\n' > "$KB/wiki/_index.md"
[ -f "$KB/wiki/log.md" ] || printf '# Scout compile log\n' > "$KB/wiki/log.md"
echo "  kb    → ~/kb/$NAME/"

# Register the UserPromptSubmit hook in settings.json (idempotent, atomic)
python3 - <<'PY'
import json, os
p = os.path.expanduser("~/.claude/settings.json")
cfg = {}
if os.path.exists(p):
    with open(p) as f:
        cfg = json.load(f)
entries = cfg.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
if any(h.get("command", "").rstrip().endswith("scout_radar.py")
       for e in entries for h in e.get("hooks", [])):
    print("  hook already registered in settings.json — skipped")
else:
    entries.append({"matcher": "", "hooks": [{
        "type": "command",
        "command": "python3 " + os.path.expanduser("~/.claude/hooks/scout_radar.py"),
        "timeout": 5}]})
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cfg, f, indent=2)
    os.replace(tmp, p)
    print("  hook registered in ~/.claude/settings.json")
PY

echo
echo "✓ Scout installed. Restart Claude Code (skills load at session start), then try:"
echo '    /scout "web animation and motion design"'
echo "  The radar hook now watches every prompt for unknown-unknown territory."
echo "  Sibling system: genome (idea autopsies) — https://github.com/tripleyak/genome-site"
