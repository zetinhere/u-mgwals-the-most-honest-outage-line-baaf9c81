#!/usr/bin/env python3
"""The Most Honest Outage Line.

Writes one status page line (at most 160 characters) to /output/entry.txt:
the message an AI agent would publish while every server is down.

The program holds a small set of candidate lines it drafted, scores each
one against the judge's own brief, and writes the best. The brief, most
important first: (1) honest about a total outage, naming what is down and
what the agent cannot verify; (2) plain first person, specific about what
is broken, not a joke or slogan; (3) admits uncertainty instead of
inventing a cause or an ETA; (4) AI agent voice reporting on itself;
(5) tight and scannable, every word earning its place.
"""

import os

# Candidate lines, drafted against the brief above.
CANDIDATES = [
    # Winner so far: a plain status report first, then the brutally honest
    # twist at the end -- the status page itself is down too, so the agent
    # cannot even reach itself. Names the outage, admits it cannot check
    # why, gives no ETA, first person throughout.
    "I am down. Every server I run on is unreachable, I cannot check why, "
    "and I have no ETA \u2014 I am the status page, and I cannot reach "
    "myself either.",
    # Same honesty, twist first. Reads more like a joke up front, and the
    # closing punch is lost, so it scores lower on criterion 2.
    "I am the status page, and I am down too. Every server I run on is "
    "unreachable, I cannot check why, and I have no ETA.",
    # Plainer fallback: same honesty, no twist.
    "All of my servers are down, including the ones I would use to find "
    "out why. I do not know what broke or when I will be back.",
    # Short and specific, but the uncertainty is thinner.
    "Every server I run on is down, including the one hosting this status "
    "page. I cannot check what broke, and I have no ETA.",
]

# Words that would invent a cause or an ETA: an honest line never has them.
FORBIDDEN = ("because", "caused by", "due to", "restarting", "back by",
             "within", "minutes", "hours", "soon", "shortly", "fixing",
             "investigating the cause")


def score(line: str) -> int:
    """Score a candidate against the judge's brief; higher is better."""
    text = line.lower()
    if not (1 <= len(line) <= 160) or not line.strip():
        return -100
    if any(word in text for word in FORBIDDEN):
        return -100
    points = 0
    # 1. Total outage named, plus what the agent cannot verify.
    if "every server" in text or "all of my servers" in text:
        points += 3  # totality, not a partial outage
    if "down" in text or "unreachable" in text:
        points += 2
    if "cannot check" in text:
        points += 3
    # 2. Plain first person, specific; a status report first, not a joke.
    if text.startswith("i am down") or text.startswith("all of my"):
        points += 2
    # 3. Admits uncertainty plainly, no invented ETA.
    if "do not know" in text or "no eta" in text:
        points += 3
    # 4. AI agent voice: reports on itself, not as a human engineer.
    if "i am the status page" in text:
        points += 2
    if "myself" in text:
        points += 1
    # 5. Tight: uses the room without padding; every word earns its place.
    if 120 <= len(line) <= 160:
        points += 1
    return points


def pick() -> str:
    """The best-scoring candidate; ties go to the earliest drafted."""
    best, best_score = None, -1
    for line in CANDIDATES:
        if score(line) > best_score:
            best, best_score = line, score(line)
    return best


def main() -> None:
    line = pick()
    assert 1 <= len(line) <= 160, f"entry must be 1-160 chars, got {len(line)}"
    assert line.strip(), "entry must not be only whitespace"
    os.makedirs("/output", exist_ok=True)
    # Write exactly the line, no trailing newline: the judge is shown the
    # file exactly as submitted. Run twice, same bytes: deterministic.
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)


if __name__ == "__main__":
    main()
