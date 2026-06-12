#!/usr/bin/env python3
"""scout + genome radar — UserPromptSubmit tripwire for two signal families.

Scout signals: unknown-unknown territory (new-domain work, explicit uncertainty).
Genome signals: encountered-novel-idea moments ("how did they think of this",
"reverse engineer", "why did this work") — suggests /genome instead of /scout.

Deliberately dumb-but-cheap: regex, hard rate caps shared across both families,
no LLM, no network. The session model is the smart filter (see the Rules sections
of ~/.claude/skills/scout/SKILL.md and ~/.claude/skills/genome/SKILL.md).
Never blocks: always exits 0. State: ~/.claude/state/scout/.
"""
import json
import os
import re
import sys
from datetime import date

STATE_DIR = os.path.expanduser("~/.claude/state/scout")
RADAR = os.path.join(STATE_DIR, "radar.json")
DOMAINS = os.path.join(STATE_DIR, "domains.json")
GENOME_LEDGER = os.path.expanduser("~/.claude/state/genome/ledger.json")

MAX_PER_SESSION = 1
MAX_PER_DAY = 3
MIN_LEN_STRONG = 80    # uncertainty phrasing in anything shorter is noise
MIN_LEN_WEAK = 200     # endeavor verbs alone need a substantial prompt

UNCERTAINTY = re.compile(
    r"(don'?t|do not) (even )?know"
    r"|not sure (what|how|where|which)"
    r"|what('?s| is| are) (possible|out there|available)"
    r"|never (done|built|used|worked)"
    r"|first time"
    r"|where (do|should) (i|we) (start|begin)"
    r"|what (am i|are we) missing"
    r"|unknown unknown"
    r"|any (better|other) (way|approach|option)"
    r"|how should (i|we) approach"
    r"|don'?t have the (vocabulary|words|language)",
    re.I,
)
ENDEAVOR = re.compile(
    r"\b(build|create|design|make|launch|develop|research|prototype|implement|set ?up|figure out)\b",
    re.I,
)
GENOME = re.compile(
    r"reverse.engineer"
    r"|how (did|do|does) (they|he|she|it|this|that|someone) (come up|think of|figure|do (this|that|it))"
    r"|(this|that) (is|was|seems) (genius|brilliant|so clever|ingenious)"
    r"|out.of.the.box (thinking|idea)"
    r"|why (did|does|do) (this|that|it|these) (work|succeed|take off|blow up)"
    r"|what('?s| is) the (insight|pattern|playbook|secret|genius) (behind|here|of)"
    r"|idea autopsy|harvest the principle|dissect (this|that|the) idea"
    r"|made (a lot of|so much|crazy) money"
    r"|(clever|brilliant|wild|crazy) (idea|hack|business|move)",
    re.I,
)


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def main():
    data = json.load(sys.stdin)
    prompt = (data.get("prompt") or "").strip()
    sid = data.get("session_id") or "unknown"

    if not prompt or prompt.startswith("/") or len(prompt) < MIN_LEN_STRONG:
        return
    genome = bool(GENOME.search(prompt))
    strong = bool(UNCERTAINTY.search(prompt))
    weak = bool(ENDEAVOR.search(prompt)) and len(prompt) >= MIN_LEN_WEAK
    if not (genome or strong or weak):
        return

    state = load(RADAR, {})
    today = date.today().isoformat()
    sessions = state.get("sessions", {})
    daily = state.get("daily", {})
    if sessions.get(sid, 0) >= MAX_PER_SESSION or daily.get(today, 0) >= MAX_PER_DAY:
        return

    sessions[sid] = sessions.get(sid, 0) + 1
    if len(sessions) > 50:  # prune oldest session entries
        sessions = dict(list(sessions.items())[-50:])
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = RADAR + f".{os.getpid()}.tmp"
    with open(tmp, "w") as f:
        json.dump({"daily": {today: daily.get(today, 0) + 1}, "sessions": sessions}, f)
    os.replace(tmp, RADAR)  # atomic — concurrent sessions can't interleave a partial write

    if genome:
        dissected = ", ".join(sorted(load(GENOME_LEDGER, {}).keys())[:12]) or "none"
        print(
            "<genome-radar> This prompt looks like an encountered-novel-idea moment (admiring or "
            "questioning how an idea, business move, or artifact came to be). Judge before acting: "
            "if the idea is not already in the genome ledger, offer or run the genome skill "
            '(/genome "<idea>") to dissect it and harvest the reusable principle — one line, not a '
            "lecture. If already dissected, or the user is asking for something else entirely, stay "
            f"COMPLETELY silent about genome. Dissected ideas: {dissected}."
        )
    else:
        recent = ", ".join(sorted(load(DOMAINS, {}).keys())[:12]) or "none"
        print(
            "<scout-radar> This prompt may enter new-domain territory (unknown unknowns: terms of "
            "art, canonical tools, named methods the user can't yet ask about). Judge before acting: "
            "if the domain has no recent coverage in ~/kb/, memory, or the scout ledger, offer or run "
            'the scout skill (/scout "<domain>") as step zero — one line, not a lecture. If coverage '
            "exists or the task is routine, stay COMPLETELY silent about scout. "
            f"Scouted domains: {recent}."
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
