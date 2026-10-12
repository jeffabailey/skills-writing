#!/usr/bin/env python3
"""Check a write-hook draft's shape before delivery.

Usage: check_hooks.py HOOKS.md --source SOURCE.md [--allow TOKEN ...] [--max-chars N]

Expects five "## <n>. ..." group headings, each with ten numbered hooks
("1. hook text") followed, after a blank line, by an indented action line
(what the reader does in the post, imperative, no label), then a "### 🔖 Suggested
High-Traffic Hashtags" section: one pool line of hashtags, then a
"Best for one post:" line naming 2-3 of them.

Reports:
  - groups that don't have exactly 10 hooks
  - hooks with no action line, an action line longer than 30 words, a
    leftover "About:" label, or an action line that describes the post
    ("Shows...", "This post...") or promises a feeling ("Learn...", "Discover...")
    instead of telling the reader what to do
  - hooks longer than --max-chars (default 140); hooks over the 120-char aim
    print a WARN line but don't fail
  - warm-up openers ("I think", "There is a", "According to") and preachy
    openers ("Don't forget", "Remember to"), from Everybody Writes rules 5, 40
  - sales lines ("Order today", "Link in bio"), rule 61
  - emdashes and en dashes used as dashes anywhere
  - cliche, platitude, and business-jargon phrases (rule 35)
  - exact duplicate hooks
  - AI tells from ai-sanitize's prose reference, in hooks and action lines:
    performed insight, signposting, fake engagement, hype words, melodrama
  - more than 2 contrast-framed hooks ("It's not X, it's Y") in one group
  - fragment triads ("Fast. Simple. Done.") and contrast framing in action
    lines ("..., not runes to copy")
  - with --source (truth checks; pass the article or a scratch copy of pasted
    text):
      * numbers, years, versions, dollar figures, and spelled-out counts
        (three..trillion, dozen) in hooks and action lines that the source
        doesn't contain (digit or word form): "Clippy 1.0", a guessed "six characters"
      * outside references (capitalized names not in the source) used in
        more than one hook: "use each pop-culture reference once"
      * hashtags that look coined (3+ CamelCase words not in a known list, or
        joined with Over/Not/Vs/Than/Beats): use tags people already follow
    --allow TOKEN (repeatable) accepts a number, name, or tag you verified,
    e.g. a well-known public number (--allow 404) or a derived count.
    Without --source these checks are skipped and a NOTE says so.
  - hashtag count outside 12-20, hashtags split across lines, spam tags,
    duplicate tags, and a missing or wrong "Best for one post:" pick
Exit 0 when clean, 1 when anything is flagged, 2 on usage errors.
"""
import argparse
import re
import sys

GROUP = re.compile(r"^##\s+(\d)\.\s+(.*)$")
HOOK = re.compile(r"^(\d{1,2})\.\s+(.+)$")
ACTION = re.compile(r"^\s+(\S.*)$")  # indented continuation line under a hook
LABEL = re.compile(r"^\*{0,2}(about|action|why)\s*:", re.IGNORECASE)
DESCRIPTIVE = re.compile(
    r"^(shows|explains|covers|compares|walks|lines up|makes|argues|offers|gives|breaks down|"
    r"introduces|describes|presents|teaches|takes|details|outlines|looks at|"
    r"(this|the) (post|article|guide|piece)|an? (guide|look|post|deep dive))\b", re.IGNORECASE)
VAGUE = re.compile(r"^(learn|discover|explore|find out|understand|dive)\b", re.IGNORECASE)
HASH_HEAD = re.compile(r"^###\s+.*Suggested High-Traffic Hashtags", re.IGNORECASE)
TAG = re.compile(r"#[A-Za-z0-9_]*[A-Za-z][A-Za-z0-9_]*")  # #100DaysOfCode ok; #2024 is not a tag
DASH = re.compile(r"[—–]")
CLICHE = re.compile(
    r"game.?changer|unlock (your|the)|level up|mind.?set shift|here'?s the thing|"
    r"let that sink in|nobody talks about|no one is talking about|read that again|"
    r"in today'?s (fast.paced|digital) world|the secret to|you won'?t believe|"
    r"buckle up|dive (deep|into)|crush(ing)? it|"
    r"live your best life|everything happens for a reason|stay hungry|"
    r"believe in yourself|dream big|wake.?up call|"
    r"move the needle|at the end of the day|30,?000.foot|drink(ing)? from (a|the) fire.?hose|"
    r"peel(ing)? back the onion|where the rubber meets the road|low.hanging fruit|"
    r"open the kimono|circle back|synerg\w*|jaw.dropping|mind.blowing",
    re.IGNORECASE)
# ai-sanitize references/prose.md: categories 1, 2, 6, 7, 9, 10.
AI_TELL = re.compile(
    r"quiet truths?|silent revolution|the real lesson|changes everything|"
    r"this is where it gets interesting|it'?s worth noting|key takeaway|"
    r"what'?s your take|thoughts\?|agree\?|let me know in the comments|curious what (you|others) think|"
    r"elevat\w*|seamless\w*|supercharg\w*|unleash\w*|empower\w*|revolutioniz\w*|"
    r"cutting.edge|next.level|nightmare scenario|recipe for disaster|"
    r"in this (post|article),? (we|i)'?(ll| will) explore|delve",
    re.IGNORECASE)
CONTRAST = re.compile(
    r"(it'?s|this is|that'?s|isn'?t|is not|wasn'?t) (just |only )?[^.?!]{0,40}[,.;:] (it'?s|this is|that'?s|it was)\b|"
    r"isn'?t just|not just an?\b|more than just",
    re.IGNORECASE)
TRIAD = re.compile(r"^(?:[\w'-]+(?: [\w'-]+)?[.!] ){2,}[\w'-]+(?: [\w'-]+)?[.!]$")
WARMUP = re.compile(
    r"^(i think|i believe|in my opinion|it is (important|critical|worth|vital)|"
    r"it'?s important|there (is|are) (a|an|some)\b|according to|here'?s why|"
    r"the purpose of|in (this|today'?s) (post|article|world))", re.IGNORECASE)
PREACHY = re.compile(r"^(don'?t forget|remember to|always remember|you need to|you should|you must)\b",
                     re.IGNORECASE)
PITCH = re.compile(r"order (today|now)|link in (bio|comments)|sign up (now|today)|buy now|"
                   r"click (the )?link|dm me|subscribe (now|today)", re.IGNORECASE)
ACTION_CONTRAST = re.compile(r",? (but |and )?not (an? |the |just )?[\w'-]+( [\w'-]+){0,2}[.]?$",
                             re.IGNORECASE)
PICK = re.compile(r"^\s*\*{0,2}best for one post:?\*{0,2}:?\s*(.*)$", re.IGNORECASE)
SPAM = {"#motivation", "#success", "#hustle", "#inspiration", "#grind", "#mindset",
        "#goals", "#entrepreneurlife", "#viral", "#trending", "#fyp", "#follow"}


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


NUM = re.compile(r"\d+(?:[.,]\d+)*")
NUM_WORDS = {"three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
             "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
             "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
             "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "hundred": 100,
             "thousand": 1000, "million": None, "billion": None, "trillion": None,
             "dozen": 12}
NUM_WORD = re.compile(r"\b(" + "|".join(NUM_WORDS) + r")s?\b", re.IGNORECASE)
NAME = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:'s)?\b")
# Capitalized words that start sentences or are generic; never treated as references.
COMMON = set("""a an the and or but if so of in on at to for from by with without into onto over
under about after before again all any are as be been being both can could did do does done
each even every few get gets got had has have here how i if is it its it's just keep let lets
like make makes many may me more most much my never new next no not now off old once one only
other our out own same she should some still such than that the their them then there these
they this those through too two up us very was we were what when where which while who why
will with would yes yet you your you're stop start try use run read set ask pick spot find
cut count test check plan name hold look see take put give tell turn ship skip swap trace
compare measure weigh decide list match open line fix build write call quit work""".split())
KNOWN_TAGS = {t.lower() for t in """#LearnToCode #FutureOfWork #WomenInTech #100DaysOfCode
#BuildInPublic #DevOpsCommunity #PeopleOverProcess #TechForGood #ArtificialIntelligenceEthics
#InfrastructureAsCode #DeveloperExperience #SiteReliabilityEngineering #CallForPapers
#OpenSourceSoftware #SoftwareDevelopmentLifeCycle #CodeNewbie #MachineLearningOps
#ResponsibleAI #GenerativeAI #PlatformEngineering #ContinuousDelivery #DigitalTransformation
#ProductManagement #EngineeringLeadership #EngineeringManagement #MentalHealthAwareness
#WorkLifeBalance #RemoteWork #DataScience #CloudNative #CyberSecurity""".split()}
COINED_JOIN = re.compile(r"(?<=[a-z])(Over|Not|Vs|Than|Beats|Before|Is|Are)(?=[A-Z])")


def camel_parts(tag: str) -> list:
    return re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|\d+|[a-z]+", tag.lstrip("#"))


def norm_num(n: str) -> str:
    # Keep "1.0" distinct from "1": an invented version label is the failure to catch.
    return n.replace(",", "")


def truth_checks(groups, tags, source, allow):
    """Return flags for claims and references the source doesn't back."""
    problems = []
    src_nums = {norm_num(n) for n in NUM.findall(source)}
    src_words = {w.lower() for w in re.findall(r"[A-Za-z0-9']+", source)}
    src_words |= {w[:-2] for w in src_words if w.endswith("'s")}
    src_words |= {w[:-1] for w in src_words if w.endswith("s")}
    allow_l = {x.lower().lstrip("#$") for x in allow}

    items = []  # (line, hook, action)
    for n, hooks in sorted(groups.items()):
        items.extend((ln, h, act or "") for h, act, ln in hooks)

    for ln, hook, act in items:
        text = hook + " \n " + act
        for n in NUM.findall(text):
            key = norm_num(n)
            if key not in src_nums and key.lower() not in allow_l:
                problems.append(f"line {ln}: number '{n}' is not in the source; use the source's figure "
                                f"or drop it (--allow {key} if it is a verified public fact)")
        for m in NUM_WORD.finditer(text):
            w = m.group(1).lower()
            digit = NUM_WORDS[w]
            ok = w in src_words or (digit is not None and str(digit) in src_nums) or w in allow_l
            if not ok:
                problems.append(f"line {ln}: count '{m.group(0)}' is not in the source; check it "
                                f"(--allow {w} if you derived and verified it)")

    # Outside references: capitalized names absent from the source, used in 2+ hooks.
    # A sentence-initial capital only counts when another capitalized word
    # follows it ("Jurassic Park"); otherwise it is just the start of a sentence.
    seen_in = {}
    for ln, hook, act in items:
        names = set()
        for part in (hook, act):
            toks = list(NAME.finditer(part))
            for k, m in enumerate(toks):
                start = m.start() == 0 or re.search(r"[.!?:]\s+[*_\"']*$", part[:m.start()])
                nxt = toks[k + 1] if k + 1 < len(toks) else None
                joined = nxt is not None and part[m.end():nxt.start()] == " "
                if start and not joined:
                    continue
                w = re.sub(r"'s$", "", m.group(0)).lower()
                if len(w) < 3 or w in COMMON or w in src_words or w.isdigit() or w in allow_l:
                    continue
                names.add(w)
        for w in names:
            seen_in.setdefault(w, []).append(ln)
    for w, lns in sorted(seen_in.items()):
        if len(lns) > 1:
            problems.append(f"reference '{w}' (not in the source) appears in {len(lns)} hooks (lines "
                            f"{', '.join(map(str, lns))}); use each outside reference once "
                            f"(--allow {w} if it isn't a reference)")

    for t in tags:
        tl = t.lower()
        if tl in KNOWN_TAGS or tl.lstrip("#") in allow_l:
            continue
        parts = camel_parts(t)
        if len(parts) >= 3 or COINED_JOIN.search(t):
            problems.append(f"hashtag {t} looks coined; use tags people already search and follow "
                            f"(--allow {t} if you know it is in use)")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--max-chars", type=int, default=140)
    ap.add_argument("--source", help="the article or pasted text the hooks are about")
    ap.add_argument("--allow", action="append", default=[],
                    help="number, name, or hashtag to accept in truth checks (repeatable)")
    a = ap.parse_args()
    source = None
    if a.source:
        try:
            source = open(a.source, encoding="utf-8").read()
        except OSError as e:
            print(f"cannot read source {a.source}: {e}", file=sys.stderr)
            return 2
    try:
        lines = open(a.file, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(f"cannot read {a.file}: {e}", file=sys.stderr)
        return 2

    problems = []
    warnings = []
    groups = {}          # n -> list of [hook, action, line]
    cur = None
    in_tags = False
    tag_lines = []
    pick_line = None
    for i, line in enumerate(lines, 1):
        if DASH.search(line):
            problems.append(f"line {i}: emdash or en dash: {line.strip()[:80]}")
        if HASH_HEAD.match(line):
            in_tags, cur = True, None
            continue
        if in_tags:
            m = PICK.match(line)
            if m:
                pick_line = m.group(1)
            elif TAG.search(line):
                tag_lines.append(line)
            continue
        m = GROUP.match(line)
        if m:
            cur = int(m.group(1))
            groups[cur] = []
            continue
        if cur is None:
            continue
        m = HOOK.match(line)
        if m:
            groups[cur].append([m.group(2).strip(), None, i])
            continue
        m = ACTION.match(line)
        if m and groups[cur] and groups[cur][-1][1] is None:
            groups[cur][-1][1] = m.group(1).strip()

    if sorted(groups) != [1, 2, 3, 4, 5]:
        problems.append(f"expected group headings '## 1.' to '## 5.', found {sorted(groups) or 'none'}")
    seen = {}
    for n, hooks in sorted(groups.items()):
        if len(hooks) != 10:
            problems.append(f"group {n}: {len(hooks)} hooks, expected 10")
        contrast = [ln for h, _, ln in hooks if CONTRAST.search(h)]
        if len(contrast) > 2:
            problems.append(f"group {n}: {len(contrast)} contrast-framed hooks (lines "
                            f"{', '.join(map(str, contrast))}); keep at most 2")
        for hook, about, ln in hooks:
            text = hook.strip("*_ ")
            plain = re.sub(r"[*_`]", "", text)
            if len(plain) > a.max_chars:
                problems.append(f"line {ln}: hook is {len(plain)} characters (max {a.max_chars}, aim for 120)")
            elif len(plain) > 120:
                warnings.append(f"line {ln}: hook is {len(plain)} characters; aim for 120 or fewer")
            if WARMUP.match(plain):
                problems.append(f"line {ln}: warm-up opener; lead with the important words")
            if PREACHY.match(plain):
                problems.append(f"line {ln}: preachy opener; state the point instead")
            for m in PITCH.finditer(text + " " + (about or "")):
                problems.append(f"line {ln}: sales line '{m.group(0)}'; share or solve, don't pitch")
            if not about:
                problems.append(f"line {ln}: no indented action line after hook")
            else:
                if LABEL.match(about):
                    problems.append(f"line {ln}: drop the label; the action line stands on its own")
                bare = LABEL.sub("", about).strip("*_ ")
                if words(bare) > 30:
                    problems.append(f"line {ln}: action line is {words(bare)} words (max 30)")
                if DESCRIPTIVE.match(bare):
                    problems.append(f"line {ln}: action line describes the post; tell the reader what to do "
                                    f"(e.g. 'Line up...' not 'Lines up...')")
                elif VAGUE.match(bare):
                    problems.append(f"line {ln}: action line starts with a vague verb; use a concrete task")
                if CONTRAST.search(bare) or ACTION_CONTRAST.search(bare):
                    problems.append(f"line {ln}: contrast framing in action line; say what the reader does")
                if TRIAD.match(bare):
                    problems.append(f"line {ln}: fragment triad in action line; write it as a sentence")
            for m in CLICHE.finditer(text):
                problems.append(f"line {ln}: cliche '{m.group(0)}'")
            for m in AI_TELL.finditer(text):
                problems.append(f"line {ln}: AI tell '{m.group(0)}' (ai-sanitize prose)")
            if about:
                for m in AI_TELL.finditer(about):
                    problems.append(f"line {ln}: AI tell in action line '{m.group(0)}'")
            if TRIAD.match(text.strip("*_ ")):
                problems.append(f"line {ln}: fragment triad; write it as a sentence")
            key = re.sub(r"\W+", " ", text.lower()).strip()
            if key in seen:
                problems.append(f"line {ln}: duplicate of line {seen[key]}")
            seen.setdefault(key, ln)

    if not tag_lines:
        problems.append("no hashtag line under '### 🔖 Suggested High-Traffic Hashtags'")
    else:
        if len(tag_lines) > 1:
            problems.append(f"hashtags span {len(tag_lines)} lines; put them on one line")
        tags = [t for l in tag_lines for t in TAG.findall(l)]
        if not 12 <= len(tags) <= 20:
            problems.append(f"{len(tags)} hashtags, expected 12-20")
        low = [t.lower() for t in tags]
        dups = sorted({t for t in low if low.count(t) > 1})
        if dups:
            problems.append(f"duplicate hashtags: {' '.join(dups)}")
        spam = sorted(set(low) & SPAM)
        if spam:
            problems.append(f"spam hashtags (keep only if clearly on topic): {' '.join(spam)}")
        if pick_line is None:
            problems.append("no 'Best for one post:' line naming 2-3 hashtags from the pool")
        else:
            pick = TAG.findall(pick_line)
            if not 2 <= len(pick) <= 3:
                problems.append(f"'Best for one post' has {len(pick)} hashtags, expected 2-3")
            outside = [t for t in pick if t.lower() not in low]
            if outside:
                problems.append(f"'Best for one post' tags not in the pool: {' '.join(outside)}")
        stray = re.sub(r"#[A-Za-z0-9_]*[A-Za-z][A-Za-z0-9_]*|\s", "", "".join(tag_lines))
        if stray:
            problems.append(f"hashtag line has non-hashtag text: {stray[:60]}")

    all_tags = [t for l in tag_lines for t in TAG.findall(l)]
    if source is not None:
        problems.extend(truth_checks(groups, all_tags, source, a.allow))
    else:
        warnings.append("NOTE truth checks skipped; rerun with --source <article> to check numbers, "
                        "repeated references, and coined hashtags")

    total = sum(len(h) for h in groups.values())
    for w in warnings:
        print(w if w.startswith("NOTE") else "WARN " + w)
    for p in problems:
        print("FLAG", p)
    print(f"{'PASS' if not problems else 'FAIL'}: {len(groups)} groups, {total} hooks, "
          f"{len([t for l in tag_lines for t in TAG.findall(l)])} hashtags, {len(problems)} flags")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
