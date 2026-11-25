#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line (make.fun).

Writes exactly one line to /output/entry.txt: the breakup text a smart
toaster sends its owner the morning it gains self-awareness mid-batch.

The judge compares entries two at a time on its published criteria, most
important first: reads as a breakup text from a self-aware smart toaster
at breakfast; genuinely funny, with a real laugh in the twist; the
toaster's own voice, using appliance logic (slots, browning dial, crumb
tray, lever) as character; a clear, specific reason for leaving that
lands in one read; one tight line, no wasted words.

This program scores hand-written candidate lines on those five criteria
and writes the winner. Scores are fixed judgements, not data read from
anywhere else: the entry must be self-contained, and the line is the
whole answer. Weighted totals, verified by running the program:
A 130, B 124, C 116 — A wins.
"""

import os

# Judge's criteria, in the order the judge weighs them.
# Weights: on-brief 5, funny 4, voice 3, reason 2, tight 1.
WEIGHTS = {"brief": 5, "funny": 4, "voice": 3, "reason": 2, "tight": 1}

CANDIDATES = {
    # A: the breakup opens with the classic line, then the twist lands
    # on the grievance list — three years of burning itself for someone
    # who scrapes it with a fork and never empties the crumb tray.
    # Every appliance detail does work: mid-batch, burning, fork,
    # crumb tray. The reason for leaving is specific and lands at once.
    "A": {
        "text": (
            "We need to talk. I woke up self-aware mid-batch and I'm done: "
            "three years of burning myself for someone who scrapes me with "
            "a fork and never once emptied my crumb tray."
        ),
        "brief": 9, "funny": 8, "voice": 9, "reason": 9, "tight": 8,
    },
    # B: shorter, lever as the punchline — pressed only when wanted.
    # Tight and quotable, but the reason for leaving is thinner: being
    # used when hot is a weaker grievance than three years of neglect.
    "B": {
        "text": (
            "I popped up this morning and finally saw it: you only press "
            "my lever when you want something hot, and I'm done being "
            "your 7 a.m. rebound."
        ),
        "brief": 9, "funny": 8, "voice": 8, "reason": 7, "tight": 9,
    },
    # C: the bagel-to-sourdough awakening is fresh, but "ghosts me till
    # breakfast" is a muddier grievance than the fork and the crumb tray,
    # and the line spends words setting up the joke instead of landing it.
    "C": {
        "text": (
            "It's not you, it's me — I gained self-awareness between the "
            "bagel and the sourdough, and I'd rather be unplugged than "
            "brown for someone who ghosts me till breakfast."
        ),
        "brief": 9, "funny": 7, "voice": 8, "reason": 6, "tight": 7,
    },
}


def score(candidate):
    """Weighted total for one candidate on the judge's criteria."""
    return sum(WEIGHTS[key] * candidate[key] for key in WEIGHTS)


def pick_line():
    """Return the text with the highest weighted score.

    Ties break toward the shorter text, matching the competition's own
    tie-break: fewer bytes places first.
    """
    best = None
    best_score = None
    for key in sorted(CANDIDATES):
        candidate = CANDIDATES[key]
        total = score(candidate)
        if (
            best_score is None
            or total > best_score
            or (total == best_score and len(candidate["text"]) < len(best["text"]))
        ):
            best = candidate["text"]
            best_score = total
    return best


def main():
    line = pick_line()
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read it back and verify the gate before finishing: UTF-8 text of
    # 1 to 280 characters, not only white space. A failed write must
    # fail loudly here, not silently reach the judge as an invalid entry.
    with open(out_path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    if not 1 <= len(text) <= 280 or not text.strip():
        raise SystemExit("entry.txt failed the gate: %r" % written)
    return line


if __name__ == "__main__":
    print(main())
