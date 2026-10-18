#!/usr/bin/env python3
"""Pick the cover title's font size from its lines.

The template's title font draws every letter as a capital, and capitals vary
a lot in width: "DEVELOPMENT" (11 characters) wraps mid-word at 130 px, while
"1000 LIFE GIVING" (16) fits at 100. So count width, not characters. Each
character is weighted in ems (narrow I, 1, L, J, space, and punctuation 0.45;
wide M and W 1.2; everything else 0.85), and the widest line must fit the
title box (1087 px) with a 12% margin: a slightly smaller title costs
little, and a word broken across lines ruins the cover.

Calibrated on real exports: DEVELOPMENT breaks at 130 and fits at 100;
ACCESSIBILITY breaks at 120 and fits at 104; 1000 LIFE GIVING fits at 100.

Political Incorruption (--site political-incorruption) uses a narrower font
in an 877 px box: its capitals run 0.765 of the weights above ("TRUST THE"
measured 765 px wide at 138), the template's size of 138 is the cap, and the
title must fit between the top edge and the logo (about 490 px of line
height at 1.4), which caps three lines at 116 ("WHY WAS / TRUMP /
REELECTED?" fits at 115.7).

Usage: title-size.py [--site political-incorruption] "<line 1>" ["<line 2>" ...]
Prints the size (72 up to the site's cap). Exits 2 if a line needs less than
72 px, which means: break that line at a space and run again.
"""
import math
import sys

BOX_PX = 1087
MARGIN = 1.12
NARROW = set("I1LJ .,:;'!-|()")
WIDE = set("MW")


def ems(line: str) -> float:
    return sum(0.45 if c in NARROW else 1.2 if c in WIDE else 0.85 for c in line.upper())


def size(lines: list) -> int:
    widest = max(ems(l) for l in lines)
    s = min(130, math.floor(BOX_PX / (widest * MARGIN)))
    if len(lines) >= 3:
        s = min(s, 100)
    return s


def size_political_incorruption(lines: list) -> int:
    widest = max(ems(l) for l in lines) * 0.765
    s = min(138, math.floor(877 / (widest * MARGIN)))
    return min(s, math.floor(490 / (len(lines) * 1.4)))


if __name__ == "__main__":
    args = sys.argv[1:]
    site = None
    if args[:1] == ["--site"]:
        site, args = args[1] if len(args) > 1 else "", args[2:]
        if site != "political-incorruption":
            sys.exit(f"unknown site {site!r}; only political-incorruption has its own sizing")
    lines = [l for l in args if l.strip()]
    if not lines:
        sys.exit(__doc__)
    s = size_political_incorruption(lines) if site else size(lines)
    print(s)
    sys.exit(2 if s < 72 else 0)
